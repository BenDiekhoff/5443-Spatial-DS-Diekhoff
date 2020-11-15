
import geojson
import json
from flask import Flask, jsonify,request, url_for, render_template,redirect
from flask_cors import CORS
import os,sys
from scipy.spatial import KDTree

app = Flask(__name__)
CORS(app)

coordList =[]
# Gets the list of lng lat coordinates from a geojson file
def getPoints():
    path = 'Assignments/A03/lonlat.geojson'
    if os.path.isfile(path):
        with open(path, 'r') as f:
            data = f.read()
    else:
        return jsonify({"Error":"lonlat.geojson not there!!"})

    return json.loads(data)


# Puts the lng lat coords into a KDtree
def getTree(data):
    coords = []
    for feature in data['features']:
        coords.append(feature['geometry']['coordinates'])
    tree = KDTree(coords)

    return tree, coords

# Render the map
@app.route('/', methods=['GET','POST'])
def index():
    mapbox_access_token = 'pk.eyJ1IjoiYmVuZGlla2hvZmYiLCJhIjoiY2sxcGp5bWlxMGNwbjNibGZ1cW9seDd2aSJ9.cPovo_u9sG8eOqRSCw_Cew'

    return render_template('map.html',mapbox_access_token=mapbox_access_token)

# Finds the five nearest neighbors for any point clicked on the map
@app.route('/click/')
def click():
    global coordList
    coordList = []
    searchCoords = []
    lng,lat = request.args.get("lngLat",None).split(",")

    searchCoords.append(float(lng))
    searchCoords.append(float(lat))
    distanceList, neighborList = tree.query(searchCoords,k=5,distance_upper_bound=5)

    # Prints info about the nearest neighbors and their distance. 
    for i in range(0,len(distanceList)):
        print(f"\nLng, Lat: {lng}, {lat}\nNearest neighbor: {coords[neighborList[i]]}\tDistance: {distanceList[i]}")


    # Creates a geojson object of nearest neighbors
    for i in neighborList:
        point = geojson.Point(coords[i])
        coordList.append(geojson.Feature(geometry=point,properties={'title':'x'} ))
    coordList = geojson.FeatureCollection(coordList)

    return "putting this here so the terminal doesn't throw a fit"


# Feeds the geojson data to the frontend
@app.route('/neighbors')
def showNeighbors():
    global coordList
    # print(type(coordList))
    # print(coordList)
    return coordList



if __name__ == '__main__':
    points = getPoints()
    tree, coords = getTree(points)
    app.run(host='localhost', port=8080, debug=True)
