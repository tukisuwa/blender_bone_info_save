# blender_bone_info_save

blenderにて、モデルのボーン情報とか他色々をJSONにして保存したり、それを描画するためのスクリプトとかを置くリポジトリです。

## bone_info_save.py

このスクリプトはアニメーションのフレームごとにJSONを生成します、フレーム数には気をつけてください。

blenderで読み込んで、アーマチュアを選択した状態で実行してください。

スクリプト冒頭の変数で設定できます。

・アニメーションレンダリングも同時に行うか。

・シェイプキー情報の出力をするか。

・出力する頂点グループ名（シーン内の全メッシュオブジェクトを対象にします）

・JSONの保存先パス（設定しない場合はシーンの出力パス、それも設定されていない場合はblendファイルパスが使用されます）



## json_trim.py

「bone_info_save.py」で出力したJSONのボーン名を変換しつつ、不要な情報を削除するためのスクリプトです。

指定したCSVに無いボーン情報は、除外されて保存します。

さらに、必要に応じて他のキーも除外できます。

コマンドラインから引数を付けてスクリプトを実行します。

各引数の説明:

-i, --input_dir: 入力JSONファイルが格納されているフォルダのパス (必須)

-c, --csv_path: ボーン名変換情報を記述したCSVファイルのパス (必須、「bone_name_vrm.csv」がサンプル、pmxから保存したJSONには「bone_name_pmx2vmd.csv」を使うといいかも)

-o, --output_dir: 出力JSONファイルを保存するフォルダのパス (指定しない場合は入力フォルダと同じ)

-e, --exclude_keys_file: 除外するキーが記述されたテキストファイルのパス (指定しない場合は何も削除しない、「exclude_keys.txt」がサンプル)

-s, --suffix: 出力ファイル名に付加するサフィックス (指定しない場合は'_trim'が付加される)

--no-suffix: 出力ファイル名にサフィックスを付加しない

## bone_viewer.py

そのまま実行するとGUI上で、ボーン情報などが書かれたJSONと描画手順が書かれたJSONをそれぞれ読み込んで、その描画結果を表示できます。

各JSONを設定したら更新ボタンを押してください。

引数を付けて実行すると、描画結果を画像として保存できます。

-j, --json: 入力JSONファイルのパスまたはフォルダパスを指定します。フォルダパスを指定した場合は、フォルダ内の全てのJSONファイルが処理されます。

-d, --drawing_instructions: 描画方法JSONファイルのパスを指定します。（「draw_Instructions_sample.json」がサンプル）

-o, --output: 出力画像ファイルまたはフォルダのパスを指定します。入力にフォルダパスを指定した場合は、出力にもフォルダパスを指定する必要があります。

-s, --suffix: 出力ファイル名のサフィックスを指定します。デフォルトは "_draw" です。空文字列("")を指定するとサフィックスは付加されません。

-b, --background: 背景色を指定します。"transparent" を指定すると透過PNGになります。デフォルトは "white" です。

### JSONファイルの形式について

スクリプト内の set_constants_from_json 関数で、JSONファイルの全ての要素が定数として読み込まれます。

"bones" キーの下に、描画する際の情報を配列で記述します。

index: 描画順序を示すインデックス (数値)。小さい値ほど先に描画されます。

draw_type: 描画方法の種類 ("circle", "ellipse", "line", "polyline", "rectangle", "arc", "point", "polygon", "pieslice", "chord", "bitmap", "text", "custom" など)。

color: 描画色を色名やRGBで指定します (例:red や [255, 0, 0])。

width: 線の太さなどを指定します。

radius: 円や楕円の半径を指定します。

start_angle, end_angle: 円弧などの開始角度と終了角度を指定します。

fill: 塗りつぶし色を指定します。

text: テキストを描画する場合に指定します。

font: テキストのフォントを指定します。

font_size: テキストのフォントサイズを指定します。

anchor: テキストのアンカー位置を指定します。

...: その他、描画方法によって必要なパラメータを指定します。

#### パラメータの指定には、簡単な計算式も使えます。

詳細は[描画方法JSONの書き方](/how_to_write_draw_Instructions_JSON.md)にて……
