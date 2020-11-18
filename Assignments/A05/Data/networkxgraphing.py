"""
The project is to use networkx to traverse through subset over railroads and primary roads. 
load shapefiles then traverse graph A to B. 
path of this file: 
C:\Users\Delly\Desktop\Fall2020\DrGriffin\TestingProgram\networkxgraphing.py
"""
"""
WHAT IS A SHAPEFILE?
A shapefile is a simple, non topological data structure [ shared boundary stored once for each polygon]
format for storing geometric location and attribute information of geographic features.  
The features can be represented by points, lines, or polygons[areas]
"""

import networkx as nx
import matplotlib.pyplot as plt
import geojson, gdal
import shlex, subprocess

def load_data(path):
    """
    Given a path, loads the file and handles it based on its extension type. 
    So far there is code for json and csv files.

    """
    _, ftype = os.path.splitext(path) # get fname(_), and extension

    if os.path.isfile(path):
        with open(path) as f:
            if ftype == ".geojson":   # handles json
                data = f.read()
                ogr2ogr -ntl MULTILINESTRING -skipfailures 
                    return json.loads(data)

            elif ftype == ".csv": # handles csv with csv reader
                with open(path, newline='') as csvfile:
                     data = csv.DictReader(csvfile)

                     return list(data)
    return None
# LOADS DATA 
# PR = PRIMARY ROADS
# RR = RAILROADS
PR = load_data("/Users/Delly/Desktop/Fall2020/DrGriffin/TestingProgram/Primary_Roads.geojson/Primary_Roads.geojson")
RR = laod_data("/Users/Delly/Desktop/Fall2020/DrGriffin/TestingProgram/Railroads.geojson/Railroads.geojson")