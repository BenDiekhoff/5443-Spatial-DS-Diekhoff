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
else:
    G = nx.read_shp(INPUT_SHAPEFILE, simplify=False)

print("converting map")
G = G.to_undirected()


# T = nx.minimum_spanning_tree(G,weight=str(G.edges(data=True)[2]['length']))
# nx.write_shp(T, OUTPUT)


# H = nx.Graph()
# H = H.to_undirected()

# for edge in G.edges(data=True):
#     # input(edge)
#     dist = edge[2]['length']
#     # input(dist)
#     # input(type(dist))
#     H.add_edge(edge[0], edge[1],weight = dist)

# # T = nx.minimum_spanning_tree(H)
# nx.write_shp(H,OUTPUT)

###############################################################################
print("reading cities")
with open(CITIES, "r") as f:
    cities = json.load(f)

print("making nodelist")
nodelist=[]
for feature in cities["features"]:
    coords = (feature["geometry"]["coordinates"][0] ,feature["geometry"]["coordinates"][1])
    nodelist.append(coords)

# input(len(nodelist))

# print("reading roads")
# with open (ROADS, "r") as f:
#     roads = json.load(f)

# print("making edgelist")
# edgelist=[]
# for feature in roads["features"]:
#     for coord in feature['geometry']['coordinates'][0]:
#         edgelist.append((coord[0], coord[1]))


path =[]
i = 0
max = len(nodelist)
print("calculating paths")
for node in nodelist:
    i+=1
    print(f"calculating paths for node {i} of {max}")
    for endnode in nodelist:
        try:
            # input(f"node: {node}, endnode: {endnode}")
            coords = nx.shortest_path(G, source=tuple(node), target=tuple(endnode))
            if len(coords) >1:
                path.append(coords)
            # pathSet= set(tuple(i)for i in path)
            # input(pathSet)
        
        except:
            pass

pathSet= set(tuple(i)for i in path)
print(len(pathSet))


pathJson = {
    "type": "FeatureCollection",
    "features": []
    }

pathdict = {
    'type':'Feature',
    "properties":{},
    'geometry':{
        'type': "MultiLineString", 
        "coordinates":[

        ]
    }
}

for path in pathSet:
    for coords in path:
        coords=list(coords)
        # input(coords)
    path=list(path)
    # input(path)
    # pathdict = {
    #     'type':'Feature',
    #     "properties":{},
    #     'geometry':{
    #         'type': "MultiLineString", 
    #         "coordinates":[

    #         ]
    #     }
    # }
    pathdict['geometry']['coordinates'].append(path)

    pathJson['features'].append(pathdict)



with open (OUTPUT +'/paths.geojson','w+') as f:
    data = json.dumps(pathJson)
    f.write(data)
        

