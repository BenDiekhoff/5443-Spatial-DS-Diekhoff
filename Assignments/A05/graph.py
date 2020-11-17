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

RR = "Assignments/A05/Data/railroadsBENDELLTEST_shapefiles.shp"
RRjson= 'Assignments/A05/Data/RailroadsBENDELLTEST.geojson'
GEOshp = 'Assignments/A05/Data/GEOshp.shp'
EDGES = 'Assignments/A05/Data/EDGES.shp'
VERTS = 'Assignments/A05/Data/VERTS.shp'





G = nx.read_shp(RR, simplify=False, geom_attrs=True, strict=True)
G = G.to_undirected()
nx.draw(G, with_labels=False)
plt.draw()
plt.savefig("Assignments/A05/Data/rr")


x =  [
                            30.782501666666661,
                            69.461110833333336
                        ]



y =[
                            31.091696388888884,
                            69.38627944444444
                        ]
path = nx.shortest_path(G,source=tuple(x), target=tuple(y),weight=None,method="dijkstra")
print(path)
# if isinstance(path,list):
#     for point in path:
#         results.append(list(point))
#     answer_collection["features"].append({"type":"feature",
#         "properties": {},
#         "geometry": 
#         {
#             "type": "LineString",
#             "coordinates": results
#         }
#         })


# plt.show()
# print("NODES:")
# print (G.nodes(data= False))
# print("EDGES:")
# print(G.edges(data=False))
# print("heelo")