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
INPUT_SHAPEFILE ="Assignments/A05/Data/10m_data/ne_10m_roads_north_america.shp"
OUTPUT = 'Assignments/A05/Data/10m_data/roads'

print("loading map")
G = nx.read_shp(INPUT_SHAPEFILE, simplify=True)

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
    edge = (feature['geometry']['coordinates'][0][0][0], feature['geometry']['coordinates'][0][0][1])
    edgelist.append(edge)

print("beginning haversine")
i = 0
max = len(nodelist)
for node in nodelist:
    minDist = 5
    closestEdge =(0,0)
    found = False
    i+=1
    print(f"calculating node {i} of {max}")
    for edge in edgelist:
        dist = haversine(node, edge, unit = "mi")
        if dist < minDist:
            minDist = dist
            closestEdge = edge
            found = True
    if (found == True):
        print(minDist)
        G.add_edge(node,closestEdge)

print("writing shapefile")
nx.write_shp(G, OUTPUT)

