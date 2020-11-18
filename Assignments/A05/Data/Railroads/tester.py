import os
os.environ['PROJ_LIB'] = 'C:\\Users\\Delly\\anaconda3\\envs\\SpatialDataFlask\\pkgs\\proj-7.1.0-h7d85306_1\\Library\\share\\proj'
os.environ['GDAL_DATA'] = 'C:\\Users\\Delly\\Desktop\\GDAL-3.1.3\\osgeo\\data\\proj'
import networkx as nx
import matplotlib.pyplot as plt
# from matplotlib import afm, cbook, ft2font, rcParams, get_cachedir
import gdal
from shapely.geometry import Point,shape
import fiona
import itertools
from shapely.geometry import mapping
import json
from haversine import haversine, Unit
import subprocess
# import glob
# import shapefile # install with conda

# The files 
RRBENDELL = ("Railroads.geojson/railroadsBENDELLTEST_shapefiles.shp") 
RRBENDELLjson = ("/Users/Delly/Desktop/Fall2020/DrGriffin/TestingProgram/Railroads.geojson/RailroadsBENDELLTEST.geojson")
RRSUB = ("Railroads.geojson/RailroadsSUB_shapefiles.shp")
GEOshape = ("Railroads.geojson/GEOshp.shp")


#verts = 'Ass-----/verts.shp'

# gets the points and coordinates from shapefiles 
def getPoints(file = RRBENDELL):
    lines = [shape(line['geometry']) for line in fiona.open(file)]
    endpts = [(Point(list(line.coords)[0]),Point(list(line.coords)[-1])) for line in lines]
    endpts = [pt for sublist in endpts for pt in sublist]


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

    # print(len(inters))
    # print(" ")
    # for iter in inters:
    #     print(" :",iter)
        

    # adds endpoint to intersection list
    for pt in endpts:
        if pt not in inters:
            inters.append(pt)
    # schema of the shapefile
    schema = {'geometry': 'Point','properties': {'test': 'int'}}
    # creation of the shapefile
    with fiona.open('resultBENDELL.shp','w','ESRI Shapefile', schema) as output:
        for i, pt in enumerate(inters):
            # print(i)
            print(" # ", i ," :",pt)
            output.write({'geometry':mapping(pt), 'properties':{'test':i}})
    

    G_RRSUB = nx.read_shp(file, simplify=True, geom_attrs=True, strict=True)

    # pos = {k:v for k,v in enumerate(G_RR.nodes())}

    nx.draw(G_RRSUB, with_labels = False)

    plt.draw()
    plt.savefig("rSimp")  # saves image to file
    # plt.show()
    print("NODES:")
    print (G_RRSUB.nodes(data= False))
    print("EDGES:")
    print(G_RRSUB.edges(data=False))
    print("hello")


def getLength(file=RRBENDELLjson):
    print(" ")
    print("In getLength")
    print("hello Beautiful")
    # ----- reading in file and loading it in ---------
    with open(file, 'r', encoding ='utf-8') as f:
        data = json.load(f)
        # creating list
        jsonList = []
        # lonList = []
        # latList = []
        # id for each property
        id = 0

        for  feature in data["features"]:
            length = 0
            lonList = []
            latList = []
            
            #appends longitute and lats to parralel lists
            for  coords in feature["geometry"]["coordinates"][0]:
                lonList.append(coords[0])
                latList.append(coords[1]) 
                # input(f"coordinates:{coords}")
                #print(f"coordinates: {coords}")

            # get the haversine distance between each set of coords. The sum of all distances is the distance is the distance of the entire line
            if len(lonList)== len(latList):

                #haversine requires lon lat tuples instead ot lat lon
                for i in range(len(lonList)):
                    coords1 = (latList[i], lonList[i])
                    coords2 = (latList[(i+1)% len(lonList)], lonList[(i+1)% len(lonList)]) # figures out which index will access
                    dist = haversine(coords1, coords2, unit = "mi") # distance in miles
                    length += dist

            #clean up and assign each line a unique id
            feature["properties"]["ID"] = id
            feature["properties"]["LENGTH"] = length
            id += 1
            jsonList.append(feature)
            #prints the file with the ID and LENGTH
            featureCollection={"type": "FeatureCollection","features": jsonList}
            j = json.dumps(featureCollection)
            with open(file, 'w+') as f:
                f.write(j)
        print("DONE")

            # ----- PRINTS JSON LIST ------
            # print("JSON LIST: ")
            # print(jsonList)
            # print(" ")

  
def geoToShape(file = RRBENDELLjson):
    print("IN CONVERTER")
    print(" ")

    # following code from https://stackoverflow.com/questions/44049679/geojson-to-shapefile-using-python
    with open(file, 'r') as f:
        data = json.load(f)
    with open(GEOshape, 'w+') as f:
        json.dump(data, f)
    args = ['ogr2ogr', '-f', 'ESRI Shapefile', 'Railroads.geojson/G.shp', GEOshape]
    subprocess.Popen(args)

    print("End OF CONVERTER")



# calling the function
# getLength()  # run this first 
 #getPoints()
geoToShape()
