import json
import csv
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import argparse
import os
import re

# bone_drawing_functions.py から描画関数をインポート
from bone_drawing_functions import *  

class BoneViewer:
    def __init__(self, master):
        self.master = master
        master.title("Bone Viewer")

        # キャンバスの最大サイズ
        self.max_canvas_width = 800
        self.max_canvas_height = 800

        # JSONファイルパス
        self.json_path = tk.StringVar()
        tk.Label(master, text="JSONファイルパス:").grid(row=0, column=0)
        tk.Entry(master, textvariable=self.json_path, width=50).grid(row=0, column=1)
        tk.Button(master, text="参照", command=self.browse_json).grid(row=0, column=2)

        # 描画方法JSONファイルパス
        self.drawing_instructions_path = tk.StringVar()
        tk.Label(master, text="描画方法JSONファイルパス:").grid(row=1, column=0)
        tk.Entry(master, textvariable=self.drawing_instructions_path, width=50).grid(row=1, column=1)
        tk.Button(master, text="参照", command=self.browse_drawing_instructions).grid(row=1, column=2)

        # 更新ボタン
        tk.Button(master, text="更新", command=self.update_canvas).grid(row=2, column=1)

        # キャンバス
        self.canvas = tk.Canvas(master, width=self.max_canvas_width, height=self.max_canvas_height)
        self.canvas.grid(row=3, column=0, columnspan=3)

        # 画像データ
        self.image = None
        self.photo_image = None

    def browse_json(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSONファイル", "*.json")])
        if filepath:
            self.json_path.set(filepath)

    def browse_drawing_instructions(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSONファイル", "*.json")])
        if filepath:
            self.drawing_instructions_path.set(filepath)

    def update_canvas(self):
        try:
            # JSONファイルを読み込み、定数を設定
            data = load_data_and_set_constants(self.json_path.get())

            # 定数をコンソールに表示
            # for key, value in globals().items():
            #     if key.isupper() and not key.startswith("__"):
            #         print(f"{key}: {value}")

            # カメラ情報からキャンバスサイズを取得
            width = int(CAMERA_RESOLUTION_X)
            height = int(CAMERA_RESOLUTION_Y)

            # キャンバスサイズを計算 (最大サイズを超えないように)
            canvas_width = width
            canvas_height = height
            if canvas_width > self.max_canvas_width:
                ratio = self.max_canvas_width / canvas_width
                canvas_width = self.max_canvas_width
                canvas_height = int(canvas_height * ratio)
            if canvas_height > self.max_canvas_height:
                ratio = self.max_canvas_height / canvas_height
                canvas_height = self.max_canvas_height
                canvas_width = int(canvas_width * ratio)

            # キャンバスサイズを更新
            self.canvas.config(width=canvas_width, height=canvas_height)

            # キャンバスをクリア
            self.canvas.delete("all")

            # 画像を作成 (元のサイズで作成)
            self.image = Image.new("RGB", (width, height), "white")
            draw = ImageDraw.Draw(self.image)

            # JSONからボーン情報と描画方法を読み込み、描画
            draw_bones(draw, data, width, height, self.drawing_instructions_path.get())

            # 画像をキャンバスサイズにリサイズ
            resized_image = self.image.resize((canvas_width, canvas_height))

            # 画像をキャンバスに表示
            self.photo_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        except FileNotFoundError:
            print("ファイルが見つかりません。")
        except json.JSONDecodeError:
            print("JSONファイルの形式が正しくありません。")
        except Exception as e:
            print(f"エラーが発生しました: {e}")


def load_data_and_set_constants(json_path):
    """
    JSONファイルを読み込み、定数を設定する

    Args:
        json_path (str): JSONファイルのパス

    Returns:
        dict: JSONファイルから読み込んだデータ
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    set_constants_from_json(json_path)
    return data

def draw_bones(draw, data, width, height, drawing_instructions_path):
    """
    JSONからボーン情報と描画方法を読み込み、描画する

    Args:
        draw (ImageDraw.Draw): 描画オブジェクト
        data (dict): JSONファイルから読み込んだデータ
        width (int): キャンバスの幅
        height (int): キャンバスの高さ
        drawing_instructions_path (str): 描画方法JSONファイルのパス
    """
    with open(drawing_instructions_path, 'r', encoding='utf-8') as f:
        instructions = json.load(f)

    # indexでソート
    sorted_instructions = sorted(instructions["bones"], key=lambda x: x["index"])

    for instruction in sorted_instructions:
        draw_type = instruction["draw_type"]

        # ここで呼び出される関数にグローバル変数を渡す
        if draw_type == "circle":
            draw_circle(draw, data, width, height, instruction, globals())
        elif draw_type == "ellipse":
            draw_ellipse(draw, data, width, height, instruction, globals())
        elif draw_type == "line":
            draw_line(draw, data, width, height, instruction, globals())
        elif draw_type == "polyline":
            draw_polyline(draw, data, width, height, instruction, globals())
        elif draw_type == "rectangle":
            draw_rectangle(draw, data, width, height, instruction, globals())
        elif draw_type == "arc":
            draw_arc(draw, data, width, height, instruction, globals())
        elif draw_type == "point":
            draw_point(draw, data, width, height, instruction, globals())
        elif draw_type == "polygon":
            draw_polygon(draw, data, width, height, instruction, globals())
        elif draw_type == "pieslice":
            draw_pieslice(draw, data, width, height, instruction, globals())
        elif draw_type == "chord":
            draw_chord(draw, data, width, height, instruction, globals())
        elif draw_type == "bitmap":
            draw_bitmap(draw, data, width, height, instruction, globals())
        elif draw_type == "text":
            draw_text(draw, data, width, height, instruction, globals())
        elif draw_type == "custom":
            custom_image = custom(data, width, height, instruction, globals())
            if custom_image:
                draw.bitmap((0, 0), custom_image) 


def draw_bones_on_canvas(json_path, drawing_instructions_path, output_path=None, output_suffix="_draw"):
    """
    JSONファイルと描画方法JSONファイルからボーンを描画する

    Args:
        json_path (str): 入力JSONファイルのパスまたはフォルダパス
        drawing_instructions_path (str): ボーン描画手順を記述したJSONファイルのパス
        output_path (str, optional): 出力画像ファイルのパスまたはフォルダパス. Defaults to None.
        output_suffix (str, optional): 出力ファイル名のサフィックス. Defaults to "_draw". 
                                      空文字列("")を指定するとサフィックスは付加されません.
    """
    try:
        if os.path.isdir(json_path):
            # json_path がフォルダの場合、フォルダ内の全てのJSONファイルを処理
            for filename in os.listdir(json_path):
                if filename.endswith(".json"):
                    json_file_path = os.path.join(json_path, filename)
                    output_filename = filename.replace(".json", f"{output_suffix}.png")
                    output_file_path = os.path.join(output_path, output_filename)
                    _draw_bones_from_files(
                        json_file_path, drawing_instructions_path, output_file_path)
        else:
            # json_path がファイルの場合、単一のJSONファイルを処理
            if output_path and os.path.isdir(output_path):
                output_filename = os.path.basename(json_path).replace(".json", f"{output_suffix}.png")
                output_file_path = os.path.join(output_path, output_filename)
            else:
                output_file_path = output_path
            _draw_bones_from_files(
                json_path, drawing_instructions_path, output_file_path)

    except FileNotFoundError:
        print("ファイルが見つかりません。")
    except json.JSONDecodeError:
        print("JSONファイルの形式が正しくありません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


def _draw_bones_from_files(json_file_path, drawing_instructions_path, output_file_path):
    """
    JSONファイルと描画方法JSONファイルからボーンを描画し、画像を保存または表示する

    Args:
        json_file_path (str): 入力JSONファイルのパス
        drawing_instructions_path (str): ボーン描画手順を記述したJSONファイルのパス
        output_file_path (str, optional): 出力画像ファイルのパス. Defaults to None.
    """
    try:
        # JSONファイルを読み込み、定数を設定
        data = load_data_and_set_constants(json_file_path)

        # カメラ情報からキャンバスサイズを取得
        width = int(CAMERA_RESOLUTION_X)
        height = int(CAMERA_RESOLUTION_Y)

        # 画像を作成
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        # JSONからボーン情報と描画方法を読み込み、描画
        draw_bones(draw, data, width, height, drawing_instructions_path)

        # 画像を保存または表示
        if output_file_path:
            image.save(output_file_path)
            print(f"画像を '{output_file_path}' に保存しました。")
        else:
            # GUIで表示
            root = tk.Tk()
            app = BoneViewer(root)
            app.image = image
            app.photo_image = ImageTk.PhotoImage(image)
            app.canvas.config(width=width, height=height)
            app.canvas.create_image(0, 0, anchor=tk.NW,
                                    image=app.photo_image)
            root.mainloop()

    except FileNotFoundError:
        print("ファイルが見つかりません。")
    except json.JSONDecodeError:
        print("JSONファイルの形式が正しくありません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


def set_constants_from_json(json_path):
    """
    JSONの全ての要素を定数にする（リストにも対応）

    Args:
        json_path (str): JSONファイルのパス
    """

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

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
                set_constants(item, new_prefix)
        else:
            # キー名を英数字とアンダースコアのみで構成されるように変換
            constant_name = re.sub(r"[^a-zA-Z0-9_]", "_", prefix.rstrip("_")) 
            globals()[constant_name] = data 

    set_constants(data)


if __name__ == "__main__":
    # 引数パーサーの設定
    parser = argparse.ArgumentParser(
        description="JSONファイルと描画方法JSONファイルからボーンを描画する")
    parser.add_argument("-j", "--json", help="入力JSONファイルのパスまたはフォルダパス")
    parser.add_argument(
        "-d", "--drawing_instructions", help="ボーン描画手順を記述したJSONファイルのパス")
    parser.add_argument("-o", "--output", help="出力画像ファイルまたはフォルダのパス")
    parser.add_argument("-s", "--suffix", help="出力ファイル名のサフィックス", default="_draw")
    args = parser.parse_args()

    if args.json and args.drawing_instructions and args.output:
        # JSON, 描画方法JSON, 出力先が指定されている場合は画像として保存
        draw_bones_on_canvas(args.json, args.drawing_instructions, args.output, args.suffix)
    else:
        # いずれかが指定されていない場合はGUIで表示
        root = tk.Tk()
        app = BoneViewer(root)
        root.mainloop()