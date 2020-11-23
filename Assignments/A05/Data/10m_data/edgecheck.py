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
EDGES = "Assignments/A05/Data/10m_data/roads/edges.geosjon"

print("reading graph")
G = nx.read_shp(INPUT_SHAPEFILE, simplify=False)

print("reading cities")
with open(CITIES, "r") as f:
    cities = json.load(f)

print("making nodelist")
nodelist=[]
for feature in cities["features"]:
    coords = (feature["geometry"]["coordinates"][0] ,feature["geometry"]["coordinates"][1])
    nodelist.append(coords)

with open(EDGES,"r") as f:
    edges = json.load(f)

print("making nodelist")
nodelist=[]
for feature in cities["features"]:
    coords = (feature["geometry"]["coordinates"][0] ,feature["geometry"]["coordinates"][1])
    nodelist.append(coords)
print("making edgelist")
edgelist=[]
for feature in edges["features"]:
    edge = (feature['geometry']['coordinates'][0][0][0], feature['geometry']['coordinates'][0][0][1])
    edgelist.append(edge)

i = 0
max = len(nodelist)
for node in nodelist:
    i+=1
    print(f"calculating paths for node {i}")
    for endnode in nodelist:
        try:    
            path = nx.shortest_path(G,node, endnode)
            input(path)
        except:
            pass
