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
    # coords = (feature["geometry"]["coordinates"][0] ,feature["geometry"]["coordinates"][1])
    coords = (feature["geometry"]["coordinates"][1] ,feature["geometry"]["coordinates"][0])
    nodelist.append(coords)

print("reading roads")
with open (ROADS, "r") as f:
    roads = json.load(f)

print("making edgelist")
edgelist=[]
for feature in roads["features"]:
    for coord in feature['geometry']['coordinates'][0]:
        edgelist.append((coord[1], coord[0]))

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
        dist = haversine(node, edge, unit = "mi") #haversine needs coords in lat/lon order
        if dist < minDist:
            minDist = dist
            closestEdge = edge
            found = True

    if (found == True):
        # print(minDist)

        #switching to lon/lat from lat/lon
        nodeX= node[1]
        nodeY= node[0]
        pathX= closestEdge[1]
        pathY=closestEdge[0]
        city = (nodeX,nodeY)
        cityPath = (pathX,pathY)

        G.add_edge(city,cityPath)

print("writing shapefile")
nx.write_shp(G, OUTPUT)

