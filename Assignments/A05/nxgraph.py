
import os
import networkx as nx
import matplotlib.pyplot as plt
import gdal
from shapely.geometry import Point, shape
import fiona
import itertools


# PR = "Assignments\\A05\\Data\\Primary_Roads.geojson"
RR = "Assignments/A05/Data/railroadsSUB.shp"
lines = [shape(line['geometry']) for line in fiona.open(RR)]
endpts = [(Point(list(line.coords)[0]), Point(list(line.coords)[-1])) for line  in lines]
# flatten the resulting list to a simple list of points
endpts= [pt for sublist in endpts for pt in sublist] 
# print(endpts)


inters = []
i = 0
for line1,line2 in  itertools.combinations(lines, 2):
  if  line1.intersects(line2):
    inter = line1.intersection(line2)
    if "Point" == inter.type:
        # print("1")
        inters.append(inter)
    elif "MultiPoint" == inter.type:
        print("2")
        inters.extend([pt for pt in inter])
  

# result = endpts.extend([pt for pt in inters  if pt not in endpts])
# for pt in inters:
#     print(pt)

from shapely.geometry import mapping
# schema of the shapefile
schema = {'geometry': 'Point','properties': {'test': 'int'}}
# creation of the shapefile
with fiona.open('result.shp','w','ESRI Shapefile', schema) as output:
    for i, pt in enumerate(inters):
        output.write({'geometry':mapping(pt), 'properties':{'test':i}})

# railGraph = nx.read_shp(RR, simplify=False, geom_attrs=True, strict=True)

# nx.draw(railGraph, with_labels=True)
# plt.draw()
# plt.show()
# , simplify=False, geom_attrs=True,strict=True)
# plt.savefig("Assignments/A05/Data/rr")
print("helo")

