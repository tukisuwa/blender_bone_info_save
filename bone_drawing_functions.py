from PIL import Image, ImageDraw, ImageFont
import importlib
import io


def draw_circle(draw, data, width, height, instruction, global_vars):  
    """円を描画する"""
    x = _evaluate_expression(instruction.get("x"), data, global_vars)  
    y = _evaluate_expression(instruction.get("y"), data, global_vars)  
    color = instruction.get("color", "black")  # デフォルト色を黒に設定
    size = int(instruction.get("size", 5))  # デフォルトサイズを5に設定

    if x is not None and y is not None:
        if 0 <= x < width and 0 <= y < height:
            draw.ellipse((x - size, y - size, x + size, y + size),
                         fill=color)
                     
def draw_ellipse(draw, data, width, height, instruction, global_vars):
    """楕円を描画する"""
    x = _evaluate_expression(instruction.get("x"), data, global_vars)
    y = _evaluate_expression(instruction.get("y"), data, global_vars)
    radius_x = int(instruction.get("radius_x", 25))  # x方向の半径 (デフォルト: 25)
    radius_y = int(instruction.get("radius_y", 15))  # y方向の半径 (デフォルト: 15)
    color = instruction.get("color", "black")
    fill = instruction.get("fill", None)  # 塗りつぶし色 (オプション)
    outline = instruction.get("outline", color)  # 輪郭の色 (デフォルト: colorと同じ)
    width = int(instruction.get("width", 1))  # 輪郭の太さ (デフォルト: 1)

    if x is not None and y is not None:
        if 0 <= x < width and 0 <= y < height:
            bbox = (x - radius_x, y - radius_y, x + radius_x, y + radius_y)
            draw.ellipse(bbox, fill=fill, outline=outline, width=width)

def draw_line(draw, data, width, height, instruction, global_vars):  
    """線を描画する"""
    start_x = _evaluate_expression(
        instruction.get("start_x"), data, global_vars)  
    start_y = _evaluate_expression(
        instruction.get("start_y"), data, global_vars)  
    end_x = _evaluate_expression(instruction.get("end_x"),
                                  data, global_vars)  
    end_y = _evaluate_expression(instruction.get("end_y"),
                                  data, global_vars)  
    color = instruction.get("color", "black")
    size = int(instruction.get("size", 2))

    if all([start_x, start_y, end_x, end_y]):
        draw.line((start_x, start_y, end_x, end_y), fill=color, width=size)

def draw_polyline(draw, data, width, height, instruction, global_vars):
    """複数の線分を繋げた折れ線や曲線を描画する"""
    points = []
    for i in range(1, len(instruction) // 2 + 1):  # 座標ペアをループ
        x_key = f"x{i}"
        y_key = f"y{i}"
        x = _evaluate_expression(instruction.get(x_key), data, global_vars)
        y = _evaluate_expression(instruction.get(y_key), data, global_vars)
        if x is not None and y is not None:
            points.extend([x, y])

    color = instruction.get("color", "black")
    width = int(instruction.get("width", 2))  # 線の太さ (デフォルト: 2)
    joint = instruction.get("joint", "curve")  # 線の結合方法 (デフォルト: "curve")

    if points:
        if joint == "curve":  # スムーズな曲線で描画
            draw.polygon(points, fill=None, outline=color, width=width)
        else:  # 折れ線で描画
            draw.line(points, fill=color, width=width, joint=joint)
            

def draw_rectangle(draw, data, width, height, instruction, global_vars):  
    """四角形を描画する"""
    x = _evaluate_expression(instruction.get("x"),
                             data, global_vars)  
    y = _evaluate_expression(instruction.get("y"),
                             data, global_vars)  
    rect_width = int(instruction.get("width", 10))
    rect_height = int(instruction.get("height", 5))
    color = instruction.get("color", "black")

    if x is not None and y is not None:
        if 0 <= x < width and 0 <= y < height:
            draw.rectangle((x - rect_width / 2, y - rect_height / 2,
                            x + rect_width / 2, y + rect_height / 2),
                           fill=color)


def draw_arc(draw, data, width, height, instruction, global_vars):  
    """円弧を描画する"""
    x = _evaluate_expression(instruction.get("x"),
                             data, global_vars)  
    y = _evaluate_expression(instruction.get("y"),
                             data, global_vars)  
    start_angle = int(instruction.get("start_angle", 0))
    end_angle = int(instruction.get("end_angle", 90))
    color = instruction.get("color", "black")
    arc_width = int(instruction.get("width", 50))  # 弧の幅を指定
    arc_height = int(instruction.get("height", 50))  # 弧の高さを指定

    if all([x, y]):
        # 弧の外接する矩形を計算
        bbox = (x - arc_width / 2, y - arc_height / 2,
                x + arc_width / 2, y + arc_height / 2)
        draw.arc(bbox, start_angle, end_angle, fill=color)


def draw_point(draw, data, width, height, instruction, global_vars):  
    """点を描画する"""
    x = _evaluate_expression(instruction.get("x"), data, global_vars)
    y = _evaluate_expression(instruction.get("y"), data, global_vars)
    color = instruction.get("color", "black")

    if all([x, y]):
        draw.point((x, y), fill=color)  


def draw_polygon(draw, data, width, height, instruction, global_vars):  
    """多角形を描画する"""
    points = []
    for i in range(1, len(instruction) // 2 + 1):  # 座標ペアをループ
        x_key = f"x{i}"
        y_key = f"y{i}"
        x = _evaluate_expression(
            instruction.get(x_key), data, global_vars)  
        y = _evaluate_expression(
            instruction.get(y_key), data, global_vars)  
        if x is not None and y is not None:
            points.extend([x, y])

    color = instruction.get("color", "black")
    fill = instruction.get("fill", None)  # 塗りつぶし色を指定

    if points:
        draw.polygon(points, fill=fill, outline=color)


def draw_pieslice(draw, data, width, height, instruction, global_vars):  
    """円グラフの扇形のような図形を描画する"""
    x = _evaluate_expression(instruction.get("x"),
                             data, global_vars)  
    y = _evaluate_expression(instruction.get("y"),
                             data, global_vars)  
    start_angle = int(instruction.get("start_angle", 0))
    end_angle = int(instruction.get("end_angle", 90))
    color = instruction.get("color", "black")
    radius = int(instruction.get("radius", 50))  # 扇形の半径を指定

    if all([x, y]):
        bbox = (x - radius, y - radius, x + radius, y + radius)
        draw.pieslice(bbox, start_angle, end_angle, fill=color)


def draw_chord(draw, data, width, height, instruction, global_vars):  
    """円弧の一部を描画し、弦で閉じる"""
    x = _evaluate_expression(instruction.get("x"),
                             data, global_vars)  
    y = _evaluate_expression(instruction.get("y"),
                             data, global_vars)  
    start_angle = int(instruction.get("start_angle", 0))
    end_angle = int(instruction.get("end_angle", 90))
    color = instruction.get("color", "black")
    fill = instruction.get("fill", None)  # 塗りつぶし色を指定
    radius = int(instruction.get("radius", 50))  # 円弧の半径を指定

    if all([x, y]):
        bbox = (x - radius, y - radius, x + radius, y + radius)
        draw.chord(bbox, start_angle, end_angle, fill=fill, outline=color)


def draw_bitmap(draw, data, width, height, instruction, global_vars):  
    """ビットマップ画像を描画する"""
    x = _evaluate_expression(instruction.get("x"),
                             data, global_vars)  
    y = _evaluate_expression(instruction.get("y"),
                             data, global_vars)  
    image_path = instruction.get("image_path")

    if all([x, y, image_path]):
        try:
            bitmap = Image.open(image_path).convert("1")  # 白黒に変換
            draw.bitmap((x, y), bitmap)
        except FileNotFoundError:
            print(f"画像ファイルが見つかりません: {image_path}")
        except Exception as e:
            print(f"ビットマップ画像の描画中にエラーが発生しました: {e}")


def draw_text(draw, data, width, height, instruction, global_vars):  
    """テキストを描画する (中心位置指定)"""
    x = _evaluate_expression(instruction.get("x"),
                             data, global_vars)  
    y = _evaluate_expression(instruction.get("y"),
                             data, global_vars)  
    text = instruction.get("text", "")
    color = instruction.get("color", "black")
    font_size = int(instruction.get("font_size", 12))
    font_family = instruction.get("font_family", "arial")

    if all([x, y, text]):
        try:
            font = ImageFont.truetype(font_family, font_size)
            text_width, text_height = draw.textsize(text, font=font)
            # テキストの中心位置を計算
            x -= text_width / 2
            y -= text_height / 2
            draw.text((x, y), text, fill=color, font=font)
        except OSError:
            print(f"フォントファイルが見つかりません: {font_family}")
        except Exception as e:
            print(f"テキストの描画中にエラーが発生しました: {e}")


def custom(data, width, height, instruction, global_vars):  
    """
    他のライブラリを使って描画を行う

    Args:
        data (dict): JSON データ
        width (int): 画像の幅
        height (int): 画像の高さ
        instruction (dict): 描画命令
        global_vars (dict): グローバル変数の辞書

    Returns:
        Image.Image or None: 描画結果の PIL Image オブジェクト、またはエラーが発生した場合は None
    """
    library_name = instruction.get("library")
    function_name = instruction.get("function")
    params = instruction.get("params", {})

    if not all([library_name, function_name]):
        print("ライブラリ名と関数名が指定されていません")
        return None

    try:
        # ライブラリを動的にインポート
        library = importlib.import_module(library_name)
        function = getattr(library, function_name)

        # パラメータに data, width, height, global_vars を追加
        params["data"] = data
        params["width"] = width
        params["height"] = height
        params["global_vars"] = global_vars  

        # 描画関数を実行
        result = function(**params)

        # 描画結果を PIL Image オブジェクトに変換
        if isinstance(result, bytes):
            # バイトストリームとして結果を受け取った場合
            image = Image.open(io.BytesIO(result))
        elif hasattr(result, "savefig"):
            # matplotlib の Figure オブジェクトなど、savefig メソッドを持つオブジェクトの場合
            buffer = io.BytesIO()
            result.savefig(buffer, format="png")
            buffer.seek(0)
            image = Image.open(buffer)
        else:
            print("描画結果を PIL Image オブジェクトに変換できません")
            return None

        return image

    except ImportError:
        print(f"ライブラリ '{library_name}' が見つかりません")
        return None
    except AttributeError:
        print(f"関数 '{function_name}' が見つかりません")
        return None
    except Exception as e:
        print(f"カスタム描画中にエラーが発生しました: {e}")
        return None


def _evaluate_expression(expression, data, global_vars):
    """式を評価する"""
    if expression is None or not isinstance(expression, str):
        return expression

    try:
        # JSONの全ての要素を定数として設定
        set_constants_from_data(data)  # この行を追加

        # 式を評価
        return eval(expression, global_vars)  # global_vars を使用して評価
    except Exception as e:
        print(f"式の評価中にエラーが発生しました: {expression} : {e}") # エラーメッセージを詳細化
        return None

def set_constants_from_data(data):
    """
    JSONデータの全ての要素を定数にする（リストにも対応）

    Args:
        data (dict or list): JSONデータ
    """

    def set_constants(data, prefix=""):
        """
        再帰的にJSONデータを走査して定数を設定する

        Args:
            data (dict or list): JSONデータ
            prefix (str): 定数名のプレフィックス
        """
        if isinstance(data, dict):
            for key, value in data.items():
                new_prefix = f"{prefix}{key.upper()}_" if prefix else f"{key.upper()}_"
                set_constants(value, new_prefix)
        elif isinstance(data, list):
            for i, item in enumerate(data):  # リストの要素にアクセス
                new_prefix = f"{prefix}{i}_" 
                set_constants(item, new_prefix)  # 各要素に対して再帰的に定数を設定
        else:
            constant_name = prefix.rstrip("_")
            globals()[constant_name] = data  # グローバル変数に設定

    set_constants(data)