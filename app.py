from flask import Flask, render_template, request, redirect
import pandas as pd
import html
import glob
import json
import numpy as np
import os
import geopandas as gpd
from shapely.geometry import Point


# JSONファイルが保存されているフォルダのパス
data_folder = "jsonfile"

# 空のGeoDataFrameを作成
all_population_gdf = gpd.GeoDataFrame()

# 各ファイルごとのデータを格納するリスト
file_population_data = []

# フォルダ内の全JSONファイルを読み込む
for file_name in os.listdir(data_folder):
    if file_name.endswith(".json"):  # JSONファイルのみ対象
        file_path = os.path.join(data_folder, file_name)
        
        # GeoJSONデータを読み込む
        temp_gdf = gpd.read_file(file_path)
        
        # ファイル名をカラムとして追加する
        temp_gdf['source_file'] = file_name
        
        # GeoDataFrameに追加
        all_population_gdf = gpd.GeoDataFrame(pd.concat([all_population_gdf, temp_gdf], ignore_index=True))

# 座標系をメートル単位のEPSG:3857に変換
all_population_gdf = all_population_gdf.to_crs(epsg=3857)
application = Flask(__name__)
print("app")
#参考 https://ihoujin.nagoya/gait-speed/
apv = {
       "20e" : {"m" : 87.6, "w" : 74.1},
       "20l" : {"m" : 85.2, "w" : 74.2},
       "30e" : {"m" : 95.5, "w" : 72.2},
       "30l" : {"m" : 85.3, "w" : 67.2},
       "40e" : {"m" : 82.3, "w" : 71.0},
       "40l" : {"m" : 82.5, "w" : 78.6},
       "50e" : {"m" : 77.8, "w" : 67.2},
       "50l" : {"m" : 72.6, "w" : 63.5},
       "60e" : {"m" : 70.1, "w" : 59.2},
       "60l" : {"m" : 63.8, "w" : 59.8},
       "70e" : {"m" : 60.7, "w" : 55.0},
       "70l" : {"m" : 54.5, "w" : 50.7},
       }
#参考 https://nuclearsecrecy.com/nukemap/
bom = {"North Korea weapon tested in 2013(10kt)": {
        "r1" : {"dist" : 153},
        "r2" : {"dist" : 1050},
        "r3" : {"dist" : 1510},
        "r4" : {"dist" : 1530},
        "r5" : {"dist" : 5700}}
       ,
       "Little Boy - Hiroshima bomb(15kt)": {
        "r1" : {"dist" : 153},
        "r2" : {"dist" : 1050},
        "r3" : {"dist" : 1510},
        "r4" : {"dist" : 1530},
        "r5" : {"dist" : 4260}}
       ,
       "Fat man - Nagasaki bomb(20kt)": {
        "r1" : {"dist" : 760},
        "r2" : {"dist" : 1310},
        "r3" : {"dist" : 1720},
        "r4" : {"dist" : 2210},
        "r5" : {"dist" : 4590}}
        ,
        "virtual bomb(50kt)": {
        "r1" : {"dist" : 292},
        "r2" : {"dist" : 1160},
        "r3" : {"dist" : 2590},
        "r4" : {"dist" : 3200},
        "r5" : {"dist" : 7280}}
        ,
        "virtual bomb(100kt)": {
        "r1" : {"dist" : 423},
        "r2" : {"dist" : 1110},
        "r3" : {"dist" : 3260},
        "r4" : {"dist" : 4380},
        "r5" : {"dist" : 9180}}
        ,
        "virtual bomb(150kt)": {
        "r1" : {"dist" : 498},
        "r2" : {"dist" : 1000},
        "r3" : {"dist" : 3740},
        "r4" : {"dist" : 5260},
        "r5" : {"dist" : 10050}}
        ,
        "virtual bomb(200kt)": {
        "r1" : {"dist" : 560},
        "r2" : {"dist" : 870},
        "r3" : {"dist" : 4110},
        "r4" : {"dist" : 5980},
        "r5" : {"dist" : 11600}}
        ,
        "virtual bomb(250kt)": {
        "r1" : {"dist" : 610},
        "r2" : {"dist" : 700},
        "r3" : {"dist" : 4430},
        "r4" : {"dist" : 6610},
        "r5" : {"dist" : 12500}}
        ,
        "virtual bomb(300kt)": {
        "r1" : {"dist" : 463},
        "r2" : {"dist" : 660},
        "r3" : {"dist" : 4710},
        "r4" : {"dist" : 7170},
        "r5" : {"dist" : 13200}}
        ,
        "virtual bomb(350kt)": {
        "r1" : {"dist" : 700},
        "r2" : {"dist" : 4950},
        "r3" : {"dist" : 7670},
        "r4" : {"dist" : 13900},
        "r5" : {"dist" : 13900}}
        ,
        "virtual bomb(400kt)": {
        "r1" : {"dist" : 740},
        "r2" : {"dist" : 5180},
        "r3" : {"dist" : 8140},
        "r4" : {"dist" : 14600},
        "r5" : {"dist" : 14600}}
        ,
        "virtual bomb(450kt)": {
        "r1" : {"dist" : 770},
        "r2" : {"dist" : 5390},
        "r3" : {"dist" : 8580},
        "r4" : {"dist" : 15100},
        "r5" : {"dist" : 15100}}
        ,
        "virtual bomb(500kt)": {
        "r1" : {"dist" : 810},
        "r2" : {"dist" : 5580},
        "r3" : {"dist" : 8990},
        "r4" : {"dist" : 15700},
        "r5" : {"dist" : 15700}}
       }
       
@application.route("/")
def hello_world():
    #dst = ""
    #point = "\t\t\tvar mpoint = ["+ html.escape(str(x)) +", "+ html.escape(str(y)) +"];"
    #for i in range(len(data)):
    #    dst = dst + "\t\t\tL.marker(["+ html.escape(str(data[i][4])) +","+ html.escape(str(data[i][5])) +"],{title:\""+ html.escape(data[i][1].replace("\n", "").replace("\r", "")) +"\"}).addTo(map);\n"
    geojsondata = []
    for file_name in os.listdir("jsonfile"): 
        f = open("jsonfile/" + file_name, "r", encoding="shift-jis")
        data = f.read()   
        data = json.loads(data)
        geojsondata.append(data)
    if request.args.get("err") is None:
        return render_template("sample2.html", geojson_data=json.dumps(geojsondata))#, dst=dst, point=point)
    else:
        if request.args.get("err") == "null":
            return render_template("sample2.html", geojson_data=json.dumps(geojsondata))#, dst=dst, point=point, err="<h2>緯度経度情報を埋めてください</h2>")
        if request.args.get("err") == "time":
            return render_template("sample2.html", geojson_data=json.dumps(geojsondata))#, dst=dst, point=point, err="<h2>避難時間の中に地下に隠れる時間を含みます</h2>")

@application.route("/bomb")
def bomb():
    x = request.args.get("ido")
    y = request.args.get("kei")
    b = request.args.get("bomb")
    point = "\t\t\tvar mpoint = ["+ html.escape(str(x)) +", "+ html.escape(str(y)) +"];"
    dst = ""
    #dst = dst + "\t\t\tL.polyline([["+ html.escape(str(sx))+","+ html.escape(str(sy))+"],["+ html.escape(str(x)) +","+ html.escape(str(y)) +"]], { color: \"#FF0000\", weight: 5 }).addTo(map);"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r1"]["dist"])) +", color: \"#000000\", fill: true, weight: 3 }).addTo(map);\n"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r2"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);\n"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r3"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);\n"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r4"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);\n"
    dst = dst + "\t\t\tL.circle(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"], { radius: "+ html.escape(str(bom[b]["r5"]["dist"]))+", color: \"#000000\", fill: true, weight: 3 }).addTo(map);\n"
    dst = dst + "\t\t\tL.marker(["+ html.escape(str(x)) +","+ html.escape(str(y)) +"],{ icon: redIcon }, {title:\"爆心地\"}).addTo(map);\n"
    #dst = dst + "\t\t\tL.circle(["+ html.escape(str(sx)) +","+ html.escape(str(sy)) +"], { radius: "+ html.escape(str(dis))+", color: \"#00FF00\", fill: true, weight: 3 }).addTo(map);"
    #dst = dst + "\t\t\tL.marker(["+ html.escape(str(sx)) +","+ html.escape(str(sy)) +"],{ icon: bkIcon }, {title:\"指定座標\"}).addTo(map);\n"
    # 任意の円の中心座標と半径（例: 東京・新宿）
    circle_center = Point(y, x)  # 防衛省
    radius = bom[b]["r5"]["dist"]  # 半径（メートル）

    # 円の作成（中心座標をEPSG:3857に変換し、bufferで円を作成）
    circle_center_3857 = gpd.GeoSeries([circle_center], crs="EPSG:4326").to_crs(epsg=3857).geometry[0]
    circle = circle_center_3857.buffer(radius)

    # 重なるポリゴンの人口計算（部分的な重なりに対応）
    partial_population = []

    for _, row in all_population_gdf.iterrows():
        if row.geometry.intersects(circle):  # 円と重なる場合
            intersection = row.geometry.intersection(circle)  # 交差部分を計算
            
            # 面積がゼロ、または交差部分が空の場合はスキップ
            if intersection.is_empty or row.geometry.area == 0:
                continue
            
            # 人口が存在する場合のみ処理する
            if 'population_max' in row and pd.notna(row['population_max']):
                # 面積の比率に基づいて人口を按分
                area_ratio = intersection.area / row.geometry.area
                population = row['population_max'] * area_ratio
                
                partial_population.append({
                    'name': row.get('source_file', 'Unknown'),  # ファイル名
                    'population': round(population) if pd.notna(population) else 0,  # 按分した人口（NaN対策）
                    'area_ratio': area_ratio                   # 重なった面積の割合
                })

    # ファイルごとの人口データを集計
    file_population_summary = {}
    for p in partial_population:
        if p['name'] in file_population_summary:
            file_population_summary[p['name']] += p['population']
        else:
            file_population_summary[p['name']] = p['population']
    dst2 = ""
    # 結果を表示
    geojsondata = []
    geojsondata2 = []
    files = []
    print("円内に含まれるデータ:")
    for file, population in file_population_summary.items():
        print(f"{file}: {population} 人")
        dst2 = dst2 + f"{file}: {population} 人<br>\n"
        files.append(file)
    for file_name in os.listdir("jsonfile"): 
        f = open("jsonfile/" + file_name, "r", encoding="shift-jis")
        data = f.read()   
        data = json.loads(data)
        if file_name not in files:
            geojsondata.append(data)
        else:
            geojsondata2.append(data)
    
    total_population = sum(p['population'] for p in partial_population)
    print(f"\n円の内部にいる合計人口: {total_population} 人")
    dst2 = dst2+ f"\n円の内部にいる合計人口: {total_population} 人"
    return render_template("sample.html",dst2 = dst2, dst=dst, point=point, geojson_data=json.dumps(geojsondata), geojson_data2=json.dumps(geojsondata2))

if __name__ == "__main__":
    application.run()
