## 描画関数のパラメータ説明とJSONサンプル(Geminiに書いてもらった)


### draw_circle

**機能:** 円を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x | 円の中心x座標 | 数値 | ○ |  |
| y | 円の中心y座標 | 数値 | ○ |  |
| color | 円の色 | 文字列 (色名または16進数) | × | "black" |
| size | 円の半径 | 数値 | × | 5 |


**JSONサンプル:**

```json
{
  "index": 0,
  "draw_type": "circle",
  "x": "HIP_CENTER_X",
  "y": "HIP_CENTER_Y",
  "color": "red",
  "size": 10
}
```


### draw_ellipse

**機能:** 楕円を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x | 楕円の中心x座標 | 数値 | ○ |  |
| y | 楕円の中心y座標 | 数値 | ○ |  |
| radius_x | x方向の半径 | 数値 | × | 25 |
| radius_y | y方向の半径 | 数値 | × | 15 |
| color | 楕円の輪郭の色 | 文字列 (色名または16進数) | × | "black" |
| fill | 楕円の塗りつぶし色 | 文字列 (色名または16進数) | × | None |
| outline | 楕円の輪郭の色 | 文字列 (色名または16進数) | × | colorと同じ |
| width | 楕円の輪郭の太さ | 数値 | × | 1 |


**JSONサンプル:**

```json
{
  "index": 1,
  "draw_type": "ellipse",
  "x": "SPINE_MID_X",
  "y": "SPINE_MID_Y",
  "radius_x": 30,
  "radius_y": 20,
  "color": "blue",
  "fill": "lightblue"
}
```


### draw_line

**機能:** 線を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| start_x | 線の始点x座標 | 数値 | ○ |  |
| start_y | 線の始点y座標 | 数値 | ○ |  |
| end_x | 線の終点x座標 | 数値 | ○ |  |
| end_y | 線の終点y座標 | 数値 | ○ |  |
| color | 線の色 | 文字列 (色名または16進数) | × | "black" |
| size | 線の太さ | 数値 | × | 2 |


**JSONサンプル:**

```json
{
  "index": 2,
  "draw_type": "line",
  "start_x": "SHOULDER_LEFT_X",
  "start_y": "SHOULDER_LEFT_Y",
  "end_x": "ELBOW_LEFT_X",
  "end_y": "ELBOW_LEFT_Y",
  "color": "green",
  "size": 3
}
```


### draw_polyline

**機能:** 複数の線分を繋げた折れ線や曲線を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x1, y1, x2, y2, ... | 線分の端点の座標を順に指定 | 数値 | ○ (最低1つの座標ペアが必要) |  |
| color | 線の色 | 文字列 (色名または16進数) | × | "black" |
| width | 線の太さ | 数値 | × | 2 |
| joint | 線の結合方法 ("curve" または "miter", "round", "bevel") | 文字列 | × | "curve" |


**JSONサンプル:**

```json
{
  "index": 3,
  "draw_type": "polyline",
  "x1": "WRIST_LEFT_X",
  "y1": "WRIST_LEFT_Y",
  "x2": "HAND_LEFT_X",
  "y2": "HAND_LEFT_Y",
  "x3": "HAND_TIP_LEFT_X",
  "y3": "HAND_TIP_LEFT_Y",
  "color": "purple",
  "width": 4,
  "joint": "round" 
}
```


### draw_rectangle

**機能:** 四角形を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x | 四角形の中心x座標 | 数値 | ○ |  |
| y | 四角形の中心y座標 | 数値 | ○ |  |
| width | 四角形の幅 | 数値 | × | 10 |
| height | 四角形の高さ | 数値 | × | 5 |
| color | 四角形の色 | 文字列 (色名または16進数) | × | "black" |


**JSONサンプル:**

```json
{
  "index": 4,
  "draw_type": "rectangle",
  "x": "ANKLE_RIGHT_X",
  "y": "ANKLE_RIGHT_Y",
  "width": 20,
  "height": 10,
  "color": "orange"
}
```


### draw_arc

**機能:** 円弧を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x | 円弧の中心x座標 | 数値 | ○ |  |
| y | 円弧の中心y座標 | 数値 | ○ |  |
| start_angle | 円弧の開始角度 (度) | 数値 | × | 0 |
| end_angle | 円弧の終了角度 (度) | 数値 | × | 90 |
| color | 円弧の色 | 文字列 (色名または16進数) | × | "black" |
| width | 円弧の幅 | 数値 | × | 50 |
| height | 円弧の高さ | 数値 | × | 50 |


**JSONサンプル:**

```json
{
  "index": 5,
  "draw_type": "arc",
  "x": "FOOT_LEFT_X",
  "y": "FOOT_LEFT_Y",
  "start_angle": 45,
  "end_angle": 135,
  "color": "brown",
  "width": 60,
  "height": 30
}
```


### draw_point

**機能:** 点を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x | 点のx座標 | 数値 | ○ |  |
| y | 点のy座標 | 数値 | ○ |  |
| color | 点の色 | 文字列 (色名または16進数) | × | "black" |


**JSONサンプル:**

```json
{
  "index": 6,
  "draw_type": "point",
  "x": "THUMB_RIGHT_X",
  "y": "THUMB_RIGHT_Y",
  "color": "gray"
}
```


### draw_polygon

**機能:** 多角形を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x1, y1, x2, y2, ... | 多角形の頂点の座標を順に指定 | 数値 | ○ (最低3つの座標ペアが必要) |  |
| color | 多角形の輪郭の色 | 文字列 (色名または16進数) | × | "black" |
| fill | 多角形の塗りつぶし色 | 文字列 (色名または16進数) | × | None |


**JSONサンプル:**

```json
{
  "index": 7,
  "draw_type": "polygon",
  "x1": 100,
  "y1": 100,
  "x2": 200,
  "y2": 150,
  "x3": 150,
  "y3": 200,
  "color": "pink",
  "fill": "lightpink"
}
```


### draw_pieslice

**機能:** 円グラフの扇形のような図形を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x | 扇形の中心x座標 | 数値 | ○ |  |
| y | 扇形の中心y座標 | 数値 | ○ |  |
| start_angle | 扇形の開始角度 (度) | 数値 | × | 0 |
| end_angle | 扇形の終了角度 (度) | 数値 | × | 90 |
| color | 扇形の色 | 文字列 (色名または16進数) | × | "black" |
| radius | 扇形の半径 | 数値 | × | 50 |


**JSONサンプル:**

```json
{
  "index": 8,
  "draw_type": "pieslice",
  "x": 250,
  "y": 250,
  "start_angle": 180,
  "end_angle": 270,
  "color": "cyan",
  "radius": 70
}
```


### draw_chord

**機能:** 円弧の一部を描画し、弦で閉じる

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x | 円弧の中心x座標 | 数値 | ○ |  |
| y | 円弧の中心y座標 | 数値 | ○ |  |
| start_angle | 円弧の開始角度 (度) | 数値 | × | 0 |
| end_angle | 円弧の終了角度 (度) | 数値 | × | 90 |
| color | 円弧の輪郭の色 | 文字列 (色名または16進数) | × | "black" |
| fill | 円弧の塗りつぶし色 | 文字列 (色名または16進数) | × | None |
| radius | 円弧の半径 | 数値 | × | 50 |


**JSONサンプル:**

```json
{
  "index": 9,
  "draw_type": "chord",
  "x": 350,
  "y": 150,
  "start_angle": 30,
  "end_angle": 150,
  "color": "magenta",
  "fill": "lightmagenta",
  "radius": 40
}
```


### draw_bitmap

**機能:** ビットマップ画像を描画する

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x | 画像の左上隅x座標 | 数値 | ○ |  |
| y | 画像の左上隅y座標 | 数値 | ○ |  |
| image_path | 画像ファイルのパス | 文字列 | ○ |  |


**JSONサンプル:**

```json
{
  "index": 10,
  "draw_type": "bitmap",
  "x": 100,
  "y": 300,
  "image_path": "path/to/your/image.bmp"
}
```


### draw_text

**機能:** テキストを描画する (中心位置指定)

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| x | テキストの中心x座標 | 数値 | ○ |  |
| y | テキストの中心y座標 | 数値 | ○ |  |
| text | 描画するテキスト | 文字列 | ○ |  |
| color | テキストの色 | 文字列 (色名または16進数) | × | "black" |
| font_size | フォントサイズ | 数値 | × | 12 |
| font_family | フォントファミリー名 | 文字列 | × | "arial" |


**JSONサンプル:**

```json
{
  "index": 11,
  "draw_type": "text",
  "x": 400,
  "y": 300,
  "text": "Hello, World!",
  "color": "darkblue",
  "font_size": 18,
  "font_family": "times new roman"
}
```


### custom

**機能:** 他のライブラリを使って描画を行う

**パラメータ:**

| パラメータ名 | 説明 | 型 | 必須 | デフォルト値 |
|---|---|---|---|---|
| library | 使用するライブラリの名前 | 文字列 | ○ |  |
| function | 使用する関数の名前 | 文字列 | ○ |  |
| params | 関数に渡すパラメータ | 辞書 | × | {} |


**JSONサンプル:**

```json
{
  "index": 12,
  "draw_type": "custom",
  "library": "matplotlib.pyplot",
  "function": "plot",
  "params": {
    "x": [1, 2, 3, 4],
    "y": [5, 6, 7, 8],
    "color": "red"
  }
}
```

**注意:**  
- `custom` 関数を使用するには、指定されたライブラリがインストールされている必要があります。
- `params` には、使用する関数に必要なパラメータを指定します。
- `data`, `width`, `height`, `global_vars` は、`custom` 関数内で自動的に `params` に追加されます。
- `custom` 関数から返される値は、`PIL.Image.Image` オブジェクト、または `bytes` オブジェクト (画像データ) である必要があります。


これらのパラメータを `drawing_instructions.json` ファイルに記述することで、骨格の描画方法をカスタマイズできます。
