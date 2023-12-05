import pandas as pd
import folium
import geopandas as gpd
import json
import numpy as np
from folium import GeoJson
from shapely.wkt import loads


tiles = "http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}"
attr = "Google"

map_gangseo=folium.Map(location=[37.5612346, 126.8228132],zoom_start=13, tiles = tiles, attr = attr)
map_gangseo.save("./map.html")


geojson_path = './najs.geojson'
with open(geojson_path, encoding='utf-8') as f:
    data = json.load(f)


geojson_layer = GeoJson(data, style_function=lambda x: {"fillColor": "blue",
                                                                "color": "gray",
                                                                "weight": 1,
                                                                "fillOpacity": 0.1}).add_to(map_gangseo)

gs_safetydata=pd.read_csv('./gangseo_saftyzone.csv', encoding='utf-8',engine='python')
gs_safetydata.info()



coordinates = []
for i in range(len(gs_safetydata)):
    row_polydata = gs_safetydata.loc[i, 'GEOM']
    geometry = loads(row_polydata)
    
    if geometry.geom_type == 'Polygon':
        coordinates = [list(coord)[::-1] for coord in geometry.exterior.coords]
    
    elif geometry.geom_type == 'MultiPolygon':
        coordinates = [[list(coord)[::-1] for coord in polygon.exterior.coords] for polygon in geometry.geoms]
    
    else:
        raise ValueError(f"지원되지 않는 geometry 유형: {geometry.geom_type}")


    print(coordinates)
    
    folium.Polygon(locations=coordinates, color='blue', fill=True, fill_color='red',tooltip='Polygon', fill_opacity=0.4).add_to(map_gangseo)



map_gangseo.save('./polygontest.html')



