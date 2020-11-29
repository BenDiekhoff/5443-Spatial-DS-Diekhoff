import os
import networkx as nx
import matplotlib.pyplot as plt
import gdal
from shapely.geometry import Point, shape, mapping
import fiona
import itertools
import json
from haversine import haversine, Unit
import subprocess
import glob
import shapefile

CITIES = "Assignments/A05/Data/10m_data/cities.geojson"
ROADS = "Assignments/A05/Data/10m_data/roads.geojson"
INPUT_SHAPEFILE ="Assignments/A05/Data/10m_data/roads/edges.shp"
OUTPUT = 'Assignments/A05/Data/10m_data/roads'
# OUTPUT = 'Assignments/A05/Data/10m_data/roads2'

print("loading map")
if OUTPUT =='Assignments/A05/Data/10m_data/roads':
    G = nx.read_shp(INPUT_SHAPEFILE, simplify=True)
else:
    G = nx.read_shp(INPUT_SHAPEFILE, simplify=False)

print("converting map")
G = G.to_undirected()

print("reading cities")
with open(CITIES, "r") as f:
    cities = json.load(f)

print("making nodelist")
nodelist=[]
for feature in cities["features"]:
    coords = (feature["geometry"]["coordinates"][0] ,feature["geometry"]["coordinates"][1])
    nodelist.append(coords)

print("reading roads")
with open (ROADS, "r") as f:
    roads = json.load(f)

print("making edgelist")
edgelist=[]
for feature in roads["features"]:
    for coord in feature['geometry']['coordinates'][0]:
        edgelist.append((coord[0], coord[1]))

i = 0
max = len(nodelist)
for node in nodelist:
    i+=1
    print(f"calculating paths for node {i} of {max}")
    for endnode in nodelist:
        try:
            input(nx.shortest_path(G, source=tuple(node), target=tuple(endnode)))
            print(f"node: {node}, endnode: {endnode}")

            # input(path)
        except:

            pass
        # path = nx.shortest_path(G,source=tuple(x), target=tuple(y),weight=None,method="dijkstra")
        

        # try:
        #     path = nx.shortest_path(G,node, endnode)
        # except:
        #     pass
        # print(path)