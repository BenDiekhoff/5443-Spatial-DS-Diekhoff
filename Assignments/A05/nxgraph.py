
import os
os.environ['PROJ_LIB'] = 'C:\\Users\\Ben-Study\\anaconda3\\envs\\maps2\\Library\\include\\boost\\geometry\\srs\\projections\\proj'
os.environ['GDAL_DATA'] = 'C:\\Users\\Ben-Study\\Desktop\\gdal stuff\\GDAL-3.1.3\\osgeo\\data\\proj'
import networkx as nx
import matplotlib.pyplot as plt

# PR = "Assignments\\A05\\Data\\Primary_Roads.geojson"
RR = "Assignments\\A05\\Data\\railroads.shp"

railGraph = nx.read_shp(RR)#, simplify=False, geom_attrs=True,strict=True)
print("helo")

