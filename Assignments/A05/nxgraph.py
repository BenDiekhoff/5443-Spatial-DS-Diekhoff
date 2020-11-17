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



def getPoints(file=RR):

    # PR = "Assignments\\A05\\Data\\Primary_Roads.geojson"
    

    #  following code from https://gis.stackexchange.com/questions/137909/intersecting-lines-to-get-crossings-using-python-with-qgis
    lines = [shape(line['geometry']) for line in fiona.open(file)]
    endpts = [(Point(list(line.coords)[0]), Point(list(line.coords)[-1])) for line  in lines]
    # flatten the resulting list to a simple list of points
    endpts= [pt for sublist in endpts for pt in sublist] 
    inters = []

    for line1,line2 in  itertools.combinations(lines, 2):
        if  line1.intersects(line2):
            inter = line1.intersection(line2)
            if "Point" == inter.type:
                inters.append(inter)
            elif "MultiPoint" == inter.type:
                inters.extend([pt for pt in inter])
            elif "MultiLineString" == inter.type:
                multiLine = [line for line in inter]
                first_coords = multiLine[0].coords[0]
                last_coords = multiLine[len(multiLine)-1].coords[1]
                inters.append(Point(first_coords[0], first_coords[1]))
                inters.append(Point(last_coords[0], last_coords[1]))
            elif "GeometryCollection" == inter.type:
                for geom in inter:
                    if "Point" == geom.type:
                        inters.append(geom)
                    elif "MultiPoint" == geom.type:
                        inters.extend([pt for pt in geom])
                    elif "MultiLineString" == geom.type:
                        multiLine = [line for line in geom]
                        first_coords = multiLine[0].coords[0]
                        last_coords = multiLine[len(multiLine)-1].coords[1]
                        inters.append(Point(first_coords[0], first_coords[1]))
                        inters.append(Point(last_coords[0], last_coords[1]))

    # add endpoints to intersection list
    for pt in endpts:
        if pt not in inters:
            inters.append(pt)
    # schema of the shapefile
    schema = {'geometry': 'Point','properties': {'test': 'int'}}
    # creation of the shapefile
    with fiona.open(VERTS,'w','ESRI Shapefile', schema) as output:
        for i, pt in enumerate(inters):
            print(" # ", i ," :",pt)
            output.write({'geometry':mapping(pt), 'properties':{'test':i}})


    # G = nx.read_shp(RR, simplify=True, geom_attrs=True, strict=True)
    # nx.draw(G, with_labels=False)
    # plt.draw()
    # plt.savefig("Assignments/A05/Data/rr")

    # # plt.show()
    # print("NODES:")
    # print (G.nodes(data= False))
    # print("EDGES:")
    # print(G.edges(data=False))


def getLength(file=RRjson):
    with open(file, 'r') as f:
        data = json.load(f)

    jsonList =[]

    id = 0

    for feature in data["features"]:
        length = 0
        lonList = []
        latList = []

        # append lons and lats to parallel lists
        for coords in feature["geometry"]["coordinates"][0]:
            lonList.append(coords[0])
            latList.append(coords[1])
            # print (f"coord:{coords}")

        # make sure lists are the same size
        if len(lonList) == len(latList):

            # get the haversine distance between each set of coords. The sum of all distances is the distance of the entire line
            for i in range(len(lonList)-1):
                # haversine requires lat,lon tuples
                coord1 = (latList[i], lonList[i])
                coord2 = (latList[i+1], lonList[i+1])
                dist = haversine(coord1, coord2, unit = "mi") # distance in miles
                length += dist
                # input(f"dist {i}: {dist}\n length {i}: {length}")

        # cleanup and assign each line a unique id
        feature["properties"]["ID"] = id
        feature["properties"]["LENGTH"] = length
        id += 1

        jsonList.append(feature)
        featureCollection = {"type": "FeatureCollection", "features": jsonList}


        # OVERWRITES ORIGINAL FILE!!!
        j = json.dumps(featureCollection)
        with open(file, 'w+') as f:
            f.write(j)

def geoToShape(file=RRjson):
    # following code from https://stackoverflow.com/questions/44049679/geojson-to-shapefile-using-python
    args = ['ogr2ogr', '-f', 'ESRI Shapefile', EDGES, RRjson]
    subprocess.Popen(args)

def traverse(start = 27, end = 29):
    G = nx.Graph()
    with open (RRjson,"r") as f:
        data = json.load(f)
    
    jsonlist = []
    for feature in data["features"]:
        if feature["geometry"]["type"] == "Point":
            G.add_node


#   $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\     $$\ $$\   
#   $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \    $$ \$$ \  
# $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ 
# \_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |\_$$  $$   |
# $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ $$$$$$$$$$\ 
# \_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|\_$$  $$  _|
#   $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |    $$ |$$ |  
#   \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|    \__|\__|  
                                                                                                                                                                        
                                                                                                                                                                        
                                                                                                                                                                        

# getLength()
# getPoints()
# geoToShape()
traverse()