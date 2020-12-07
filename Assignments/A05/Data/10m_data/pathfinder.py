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
# OUTPUT = 'Assignments/A05/Data/10m_data/mst'
OUTPUT = 'Assignments/A05/Data/10m_data/mst2'


print("loading map")
if OUTPUT =='Assignments/A05/Data/10m_data/mst':
    G = nx.read_shp(INPUT_SHAPEFILE, simplify=True)
    print(G)
else:
    G = nx.read_shp(INPUT_SHAPEFILE, simplify=False)
    print(G)

# wichitaFalls = (-98.493068483253921, 33.913626321441143)
# sanFran = (-122.417168773552248, 37.769195629687431)
#tallahasee & daytonabeach -81.671932676760491, 30.331966629909687 
shawnee= (-96.9337838152789, 35.342789732905317)
mcalester= ( -95.765973960131021, 34.932995624830539)

fw = (-97.340038087741448, 32.739977029444219)
dal = (-96.841962787498176, 32.821969681677331)
path = nx.shortest_path(G,shawnee)
path2 = nx.shortest_path(G,shawnee, mcalester)
# path = nx.shortest_path(G,mcalester,shawnee)
# path2 = nx.dijkstra_path(G,shawnee,mcalester)
print(path2)