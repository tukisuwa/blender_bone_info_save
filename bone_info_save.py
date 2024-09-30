import bpy
import json
import os
import mathutils
from bpy_extras.object_utils import world_to_camera_view

# モード選択 (レンダリングモード: True, フレーム保存モード: False)
rendering_mode = False

# シェイプキー情報を出力するかどうか
export_shape_keys = True

def get_bone_chain_global_locations(armature_object):
    """
    アーマチュアオブジェクトの全てのボーンについて、
    ルートボーンから順に末端ボーンまでのグローバル座標を取得する

    Args:
        armature_object (bpy.types.Object): アーマチュアオブジェクト

    Returns:
        dict: ボーン名とその子ボーンのグローバル座標を格納した辞書
    """

    bone_data = {}

    def traverse_bones(bone):
        """
        ボーン階層を再帰的にたどり、各ボーンのグローバル座標を取得する

        Args:
            bone (bpy.types.PoseBone): ボーン
        """

        global_matrix = armature_object.matrix_world @ bone.matrix
        global_location = list(global_matrix.translation)  # ベクトルをリストに変換

        bone_data[bone.name] = {
            "global_coords": global_location, 
        }

        for child in bone.children:
            traverse_bones(child)

    # ルートボーンから処理を開始
    for root_bone in armature_object.pose.bones:
        if not root_bone.parent:
            traverse_bones(root_bone)

    return bone_data

def get_camera_info(camera_object, resolution_x, resolution_y):
    """
    カメラオブジェクトの情報（位置、回転、焦点距離、レンダリング解像度）を取得する

    Args:
        camera_object (bpy.types.Object): カメラオブジェクト
        resolution_x (int): レンダリングの横幅 (ピクセル数)
        resolution_y (int): レンダリングの縦幅 (ピクセル数)

    Returns:
        dict: カメラの情報を含む辞書
    """
    camera_data = {}
    camera_data["location"] = list(camera_object.location)
    camera_data["rotation_euler"] = list(camera_object.rotation_euler)
    camera_data["focal_length"] = camera_object.data.lens
    # 解像度を追加
    camera_data["resolution_x"] = resolution_x
    camera_data["resolution_y"] = resolution_y
    return camera_data

def get_2d_screen_coords(scene, world_coords, cam):
    """
    3D空間上のワールド座標を、カメラのビューポート上の2D座標に変換する

    Args:
        scene (bpy.types.Scene): Blenderのシーンデータ
        world_coords (Vector): 3Dワールド座標
        cam (bpy.types.Object): カメラオブジェクト

    Returns:
        tuple: 2D座標(x, y)
               ビューポートの外側でも座標を計算し、負の値も許容する
    """

    # ワールド座標をカメラのビューポート座標に変換
    co_2d = world_to_camera_view(scene, cam, world_coords)

    # ビューポート座標をスクリーン座標に変換 
    render_scale = scene.render.resolution_percentage / 100
    screen_width = scene.render.resolution_x * render_scale
    screen_height = scene.render.resolution_y * render_scale

    # カメラのタイプを取得
    camera_type = cam.data.type

    if camera_type == 'PERSP':
        # 透視投影の場合
        if co_2d.z > 0:
            screen_x = round(co_2d.x * screen_width)
            screen_y = round((1 - co_2d.y) * screen_height)  # Y座標を反転
        else:
            screen_x = -1  # 画面外の場合は-1を返す
            screen_y = -1
    elif camera_type == 'ORTHO':
        # 平行投影の場合
        screen_x = round(co_2d.x * screen_width)
        screen_y = round((1 - co_2d.y) * screen_height)  # Y座標を反転
    else:
        screen_x = -1  # 未知のカメラタイプの場合は-1を返す
        screen_y = -1

    return (screen_x, screen_y)

def get_vertex_group_screen_coords(obj, vertex_group_name, scene, cam):
    """
    特定の頂点グループに属する頂点のスクリーン座標とグローバル座標を取得する

    Args:
        obj (bpy.types.Object): オブジェクト
        vertex_group_name (str): 頂点グループ名
        scene (bpy.types.Scene): シーン
        cam (bpy.types.Object): カメラ

    Returns:
        list: スクリーン座標とグローバル座標のリスト
    """

    if vertex_group_name not in obj.vertex_groups:
        print(f"頂点グループ '{vertex_group_name}' はオブジェクト '{obj.name}' に存在しません。スキップします。")
        return [], [] # 頂点グループが存在しない場合は空のリストを返す

    vertex_group_index = obj.vertex_groups[vertex_group_name].index
    screen_coords = []

    # depsgraphを取得
    depsgraph = bpy.context.evaluated_depsgraph_get()
    # 評価後のメッシュデータを取得
    evaluated_object = obj.evaluated_get(depsgraph)
    evaluated_mesh = evaluated_object.data

    for vertex in obj.data.vertices:
        for group in vertex.groups:
            if group.group == vertex_group_index and group.weight > 0:
                # 変形後の頂点座標を取得
                world_coords = obj.matrix_world @ evaluated_mesh.vertices[vertex.index].co 
                screen_coord = get_2d_screen_coords(scene, world_coords, cam)
                screen_coords.append({
                    "vertex_index": vertex.index, 
                    "screen_coords": screen_coord,
                    "global_coords": list(world_coords) 
                })
                break # 同じ頂点が複数の頂点グループに属している場合、最初の頂点グループのみ処理する

    # 辺のスクリーン座標も取得 (変形後の頂点座標を使用)
    edge_screen_coords = []
    for edge in obj.data.edges:
        v1_index = edge.vertices[0]
        v2_index = edge.vertices[1]
        v1_screen_coord = None
        v2_screen_coord = None

        for coord in screen_coords:
            if coord["vertex_index"] == v1_index:
                v1_screen_coord = coord["screen_coords"]
            if coord["vertex_index"] == v2_index:
                v2_screen_coord = coord["screen_coords"]

        if v1_screen_coord and v2_screen_coord:
            edge_screen_coords.append({"edge_index": edge.index, "screen_coords": [v1_screen_coord, v2_screen_coord]})

    return screen_coords, edge_screen_coords


def save_frame_data_core(scene, frame):

    # scene (bpy.types.Scene): Blenderのシーンデータ
    # frame (int): 保存するフレーム番号


    # フレーム番号を設定
    scene.frame_set(frame)

    # オブジェクトの状態を更新
    bpy.context.view_layer.update()

    # データを格納する辞書
    output_data = {}

    # アーマチュアオブジェクトを取得
    armature_object = None
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE':
            armature_object = obj
            break

    # アーマチュアの情報
    if armature_object:
        # ボーンのグローバル座標を取得
        bone_data = get_bone_chain_global_locations(armature_object)

        # 各ボーンの2Dスクリーン座標とhead/tailのグローバル座標を追加
        for bone_name, bone_info in bone_data.items():
            bone = armature_object.pose.bones[bone_name]

            # ボーンのhead位置をワールド座標に変換
            head_world_coords = armature_object.matrix_world @ bone.head

            # ボーンのtail位置をワールド座標に変換
            tail_world_coords = armature_object.matrix_world @ bone.tail

            # 2Dスクリーン座標を取得 (headのみ)
            screen_coords = get_2d_screen_coords(scene, head_world_coords, scene.camera)

            # tailの2Dスクリーン座標を取得
            tail_screen_coords = get_2d_screen_coords(scene, tail_world_coords, scene.camera)

            # スクリーン座標とグローバル座標を辞書に追加
            bone_info["global_coords"] = list(head_world_coords)  
            bone_info["screen_coords"] = screen_coords 
            bone_info["tail_global_coords"] = list(tail_world_coords)
            bone_info["tail_screen_coords"] = tail_screen_coords

        # 子ボーンの情報を追加
        for bone_name, bone_info in bone_data.items():
            bone = armature_object.pose.bones[bone_name] # ループ内でbone変数を更新
            bone_info["children"] = [] # ここでchildrenを追加
            for child in bone.children: 
                bone_info["children"].append(child.name)

        output_data["bones"] = bone_data
    else:
        print("アーマチュアが見つかりません。")

    # シーン内のアクティブカメラを取得
    camera_object = scene.camera

    # カメラ情報が取得できた場合のみ出力
    if camera_object:
        # レンダリング解像度を取得
        resolution_x = scene.render.resolution_x * scene.render.resolution_percentage / 100
        resolution_y = scene.render.resolution_y * scene.render.resolution_percentage / 100

        output_data["camera"] = get_camera_info(camera_object, resolution_x, resolution_y)

    # 特定の頂点グループのスクリーン座標を取得
    vertex_group_names = ["group1", "group2", "group3"] # 対象の頂点グループ名のリスト

    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.vertex_groups:  # メッシュオブジェクトかつ頂点グループを持つ場合のみ
            for vertex_group_name in vertex_group_names:
                vertex_screen_coords, edge_screen_coords = get_vertex_group_screen_coords(obj, vertex_group_name, scene, scene.camera)
                if vertex_screen_coords: # 頂点グループが存在する場合のみJSONに追加
                    output_data[vertex_group_name] = {
                        "vertices": vertex_screen_coords,
                        "edges": edge_screen_coords
                    }

    # シェイプキーの情報 (export_shape_keys が True の場合のみ)
    if armature_object and export_shape_keys:
        shape_key_data = {}
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.find_armature() == armature_object:
                if obj.data.shape_keys:
                    obj_shape_key_data = {}
                    for shape_key in obj.data.shape_keys.key_blocks:
                        if shape_key.name != 'Basis':
                            obj_shape_key_data[shape_key.name] = shape_key.value
                    # メッシュオブジェクトが複数ある場合はオブジェクト名を追加
                    if len(shape_key_data) > 0:
                        shape_key_data[f"shape_keys_{obj.name}"] = obj_shape_key_data
                    else:
                        shape_key_data = obj_shape_key_data  # 最初のオブジェクトはそのまま
        if shape_key_data:  # shape_key_dataが空でない場合のみ出力に追加
            output_data["shape_keys"] = shape_key_data

    # レンダー出力パスを取得 (シーンの設定を使用)
    output_path = scene.render.filepath

    # 出力パスが設定されていない場合は、ブレンドファイルと同じディレクトリを使用
    if not output_path:
        output_path = bpy.path.abspath("//")

    # フレーム番号を取得
    frame = scene.frame_current

    # ファイル名と拡張子を取得
    file_name, file_ext = os.path.splitext(os.path.basename(output_path))

    # JSONファイル名を作成
    json_file_name = f"{frame:04d}.json"

    # JSONファイルパスを作成
    json_file_path = os.path.join(os.path.dirname(output_path), json_file_name) # dirnameを追加

    # JSONデータを出力
    with open(json_file_path, "w", encoding="utf-8") as f:  # エンコーディングを指定
        json.dump(output_data, f, indent=4, ensure_ascii=False)  # ensure_ascii=False を追加

    # 進捗状況を表示
    total_frames = scene.frame_end - scene.frame_start + 1
    print(f"フレーム {frame} / {total_frames} のデータを '{json_file_path}' に保存しました。")

def render_and_save_data(scene):
    """
    レンダリング後のフレームデータを保存する
    """
    save_frame_data_core(scene, scene.frame_current)

def save_frame_data(scene, frame):
    """
    指定されたフレームのデータを保存する
    """
    save_frame_data_core(scene, frame)


def main():
    """
    メイン関数: レンダリングモードまたはフレーム保存モードを実行する
    """

    scene = bpy.context.scene

    if rendering_mode:
        # レンダリングモード
        bpy.app.handlers.render_post.append(render_and_save_data)
        bpy.ops.render.render(animation=True)
        bpy.app.handlers.render_post.remove(render_and_save_data)  # ハンドラを削除
    else:
        # フレーム保存モード
        start_frame = scene.frame_start
        end_frame = scene.frame_end
        frame_step = scene.frame_step

        for frame in range(start_frame, end_frame + 1, frame_step):
            save_frame_data(scene, frame)


if __name__ == "__main__":
    main()