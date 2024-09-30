import json
import csv
import os
from collections import OrderedDict
import argparse

def extract_bone_data(input_json_path, output_json_path, csv_path, exclude_keys=None):
    """
    入力JSONファイルから指定されたボーンのデータとカメラ情報を抽出し、
    新しいボーン名でソートして新しいJSONファイルに出力する

    Args:
        input_json_path (str): 入力JSONファイルのパス
        output_json_path (str): 出力JSONファイルのパス
        csv_path (str): ボーン名変換情報を記述したCSVファイルのパス
        exclude_keys (list, optional): 除外するキーのリスト。指定しない場合は何も削除しない。Defaults to None.
    """

    # JSONファイルを読み込み
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # CSVファイルからボーン名変換情報を取得
    bone_name_mapping = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            original_name, new_name = row
            bone_name_mapping[original_name] = new_name

    # 新しいJSONファイルに出力するデータ
    output_data = {"bones": OrderedDict()}

    def remove_keys_recursive(data, exclude_keys):
        if isinstance(data, dict):
            for key in list(data.keys()):  # 削除中にエラーが出ないようにlist(data.keys())とします
                if key in exclude_keys:
                    del data[key]
                else:
                    remove_keys_recursive(data[key], exclude_keys)
        elif isinstance(data, list):
            for item in data:
                remove_keys_recursive(item, exclude_keys)

    # ボーン情報以外のデータをコピー & 不要なキーを削除
    for key, value in data.items():
        if key != "bones":
            output_data[key] = value.copy()
            if exclude_keys:
                remove_keys_recursive(output_data[key], exclude_keys)

    # 元のボーン名でループ (bonesの処理)
    for original_name in data["bones"]:
        if original_name in bone_name_mapping:
            new_bone_name = bone_name_mapping[original_name]
            output_data["bones"][new_bone_name] = data["bones"][original_name].copy()
            if exclude_keys:
                remove_keys_recursive(output_data["bones"][new_bone_name], exclude_keys)

    # JSON ファイルに出力
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # 引数パーサーの設定
    parser = argparse.ArgumentParser(description="JSONファイルからボーンデータを抽出し、ソートして新しいJSONファイルを作成する")
    parser.add_argument("-i", "--input_dir", required=True, help="入力JSONファイルが格納されているフォルダ")
    parser.add_argument("-c", "--csv_path", required=True, help="ボーン名変換情報を記述したCSVファイルのパス")
    parser.add_argument("-e", "--exclude_keys_file", help="除外するキーが記述されたテキストファイルのパス")
    parser.add_argument("-o", "--output_dir", help="出力JSONファイルを保存するフォルダ (指定しない場合は入力フォルダと同じ)", default=None)
    parser.add_argument("-s", "--suffix", help="出力ファイル名に付加するサフィックス (指定しない場合は'_trim'が付加される)", default="_trim")
    parser.add_argument("--no-suffix", help="出力ファイル名にサフィックスを付加しない", action="store_true")
    args = parser.parse_args()

    # 出力フォルダの設定
    output_dir = args.output_dir if args.output_dir else args.input_dir

    # サフィックスの設定
    if args.no_suffix:
        suffix = ""
    else:
        suffix = args.suffix

    # 除外するキーのリストを読み込み (指定がない場合はNone)
    exclude_keys = []
    if args.exclude_keys_file:
        with open(args.exclude_keys_file, 'r', encoding='utf-8') as f:
            for line in f:
                exclude_keys.append(line.strip())

    # 入力フォルダ内のJSONファイルを処理
    for filename in os.listdir(args.input_dir):
        if filename.endswith(".json"):
            input_json_path = os.path.join(args.input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + suffix + ".json"
            output_json_path = os.path.join(output_dir, output_filename)

            # JSONデータの抽出
            extract_bone_data(input_json_path, output_json_path, args.csv_path, exclude_keys)
            print(f"データを '{output_json_path}' に出力しました。")