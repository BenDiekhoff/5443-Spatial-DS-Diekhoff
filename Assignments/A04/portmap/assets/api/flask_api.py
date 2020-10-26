#!/usr/bin/env python3
import csv
import glob
import json
import os
import sys
import geojson
import rtree

from scipy.spatial import KDTree
from flask import Flask,  url_for
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask import send_file

from misc_functions import haversine, bearing

app = Flask(__name__)
CORS(app)

#
#       $$\            $$\
#       $$ |           $$ |
#  $$$$$$$ | $$$$$$\ $$$$$$\    $$$$$$\
# $$  __$$ | \____$$\_$$  _|   \____$$\
# $$ /  $$ | $$$$$$$ | $$ |     $$$$$$$ |
# $$ |  $$ |$$  __$$ | $$ |$$\ $$  __$$ |
# \$$$$$$$ |\$$$$$$$ | \$$$$  |\$$$$$$$ |
#  \_______| \_______|  \____/  \_______|
#


def load_data(path):
    """Given a path, load the file and handle it based on its extension type.
    """

    _, ftype = os.path.splitext(path)  # get fname and extension

    if os.path.isfile(path):
        with open(path) as f:

            if ftype == ".json" or ftype == ".geojson":  # handle json
                data = json.load(f)
                return data

            elif ftype == ".csv":  # handle csv with csv reader
                with open(path, newline='') as csvfile:
                    data = csv.DictReader(csvfile)
                    return list(data)
            else:
                print("neither json or csv")
                return None


UFOS = load_data('Assignments/A04/Data/ufo_data/fixed_ufos.geojson')
# EZUFOS =load_data('Assignments/A04/Data/ufo_data/ufos.geojson')
CITIES = load_data(
    'Assignments/A04/Data/countries_states/major_cities.geojson')
# # print(type(CITIES))
# CELL = load_data('Assignments/A04/Data/cellular_data/cellular.geojson')
STATE_BBOXES = load_data('Assignments/A04/Data/US_State_Bounding_Boxes.csv')
STATES = load_data('Assignments/A04/Data/countries_states/states.json')
# RRS = load_data('Assignments/A04/Data/railroads.geojson')

# setNames = ['UFOS', 'CRASHES', 'CITIES', 'CELL', 'STATE_BBOXES', 'STATES', 'RRS']
# dataSets = [UFOS, CRASHES, CITIES, CELL, STATE_BBOXES, STATES, RRS]
cityDict = {}
for city in CITIES['features']:
    if city['properties']['name'] != "line":
        cityDict[city['properties']['name']] = city['geometry']['coordinates']
CITIES = cityDict
# print(CITIES)



def getTree():
    coords = []
    for feature in UFOS['features']:
        # print(feature)
        if type(feature['geometry']['coordinates'][0]) != float or type(feature['geometry']['coordinates'][1]) != float:
            pass
        else:
            coords.append(feature['geometry']['coordinates'])
    tree = KDTree(coords)
    print("This is tree: ", tree)
    return tree, coords


def getRTree():
    idx = rtree.index.Index()
    left, bottom, right, top = (-180, -90, 180, 90)

    index = 0
    rtreeID = {}
    for feature in UFOS['features']:

        if type(feature['geometry']['coordinates'][0]) != float or type(feature['geometry']['coordinates'][1]) != float:
            pass
        else:
            left = feature['geometry']['coordinates'][0]
            right = feature['geometry']['coordinates'][0]
            bottom = feature['geometry']['coordinates'][1]
            top = feature['geometry']['coordinates'][1]
            coords = (left, bottom, right, top)
            idx.insert(index, coords)
            rtreeID[index] = feature
            index += 1

    return(idx, rtreeID)


#                                 $$\
#                                 $$ |
#  $$$$$$\   $$$$$$\  $$\   $$\ $$$$$$\    $$$$$$\   $$$$$$$\
# $$  __$$\ $$  __$$\ $$ |  $$ |\_$$  _|  $$  __$$\ $$  _____|
# $$ |  \__|$$ /  $$ |$$ |  $$ |  $$ |    $$$$$$$$ |\$$$$$$\
# $$ |      $$ |  $$ |$$ |  $$ |  $$ |$$\ $$   ____| \____$$\
# $$ |      \$$$$$$  |\$$$$$$  |  \$$$$  |\$$$$$$$\ $$$$$$$  |
# \__|       \______/  \______/    \____/  \_______|\_______/

# Render the map
@app.route('/token', methods=['GET'])
def index():
    with open('Assignments/A04/mapboxToken.txt', 'r') as f:
        mapbox_access_token = f.read()

    return mapbox_access_token


@app.route("/", methods=["GET"])
def getRoutes():
    """ getRoutes: this gets all the routes!
    """
    routes = {}
    for r in app.url_map._rules:
        routes[r.rule] = {}
        routes[r.rule]["functionName"] = r.endpoint
        routes[r.rule]["help"] = formatHelp(r.endpoint)
        routes[r.rule]["methods"] = list(r.methods)

    routes.pop("/static/<path:filename>")
    routes.pop("/")

    response = json.dumps(routes, indent=4, sort_keys=True)
    response = response.replace("\n", "<br>")
    return "<pre>"+response+"</pre>"


@app.route('/states', methods=["GET"])
def states():
    """ Description: return state menu for front end
        Params:
            None
        Example: http://localhost:8080/states?filter=<state name>
    """
    filt = request.args.get('filter', None)
    # print(filt)
    if filt:
        results = []
        for state in STATES:
            if filt.lower() == state['name'][:len(filt)].lower():
                results.append(state)
    else:
        results = STATES

    return handle_response(results)


@app.route('/state_bbox', methods=["GET"])
def state_bbox():
    """ Description: Return a bounding box for a US state
        Params:
            None
    Example: http://localhost:8080/state_bbox?state=<statename>
    """
    state = request.args.get('state', None)
    # print(f"state {state}")
    if not state:
        results = STATE_BBOXES
        return handle_response(results)

    state = state.lower()
    for row in STATE_BBOXES:
        if row['name'].lower() == state or row['abbr'].lower == state:
            row['xmax'] = float(row['xmax'])
            row['xmin'] = float(row['xmin'])
            row['ymin'] = float(row['ymin'])
            row['ymax'] = float(row['ymax'])
            results = row
    # print(f'results{results}')
    return handle_response(results)


@app.route("/dataset", methods=["GET"])
def getDataSet():
    """Loads data sets and gives each data set a source id
        Params:
            set (str): the dataset you want to load
        Example: http://localhost:8080/dataset?set=<setname>
            """
    name = request.args.get('set', None)
    global dataSets
    global setNames

    for i in range(len(setNames)):
        if name == setNames[i]:
            sid = i
            return handle_response(dataSets[sid], sid)


@app.route("/setlist", methods=["GET"])
def getSetList():
    """Sends a list of setnames to the front end
    Params:
        None
    Example: http://localhost:8080/setlist
    """
    global setNames
    # nameList = {}
    # for name, i in zip(setNames,range(len(setNames))):
    #     nameList[name] = i

    # print(nameList)
    # return handle_response(nameList)
    return handle_response(setNames)


@app.route('/neighbor', methods=["GET"])
def findNearestNeigbors():
    """ Description: Return x nearest neigbhors for give lon lat coords
        Params:
            lon: (float) longitude
            lat: (float) latitude
            num: (int) number of nearest neighbors to find
        Example: http://localhost:8080/neighbor?lon=<longitude>&lat=<latitude>&num=<number of nearest neighbors to find>
    """
    global tree
    global coords

    lon = float(request.args.get('lon', None))
    lat = float(request.args.get('lat', None))
    num = int(request.args.get('num', None))

    searchCoords = [lon, lat]  # [[98.581081, 29.38421],[98.581081, 29.38421]]
    # returns an array of distances and an array of indices for nearest neighbors
    distanceList, neighborList = tree.query(
        searchCoords, k=num, distance_upper_bound=180)

    # # prints the results of the query to the console
    # if num > 1:
    #     for i in range(0,num):
    #         print(f"\nLng, Lat: {lon}, {lat}\nNearest neighbor: {coords[neighborList[i]]}\tDistance: {distanceList[i]}")
    # else:
    #     print(f"\nLng, Lat: {lon}, {lat}\nNearest neighbor: {neighborList}\tDistance: {distanceList}")

    neighbors = []
    if num == 1:
        point = geojson.Point(coords[0])
        neighbors.append(geojson.Feature(geometry=point))

    else:
        for i in neighborList:
            # neighbors.append(coords[i])
            point = geojson.Point(coords[i])
            neighbors.append(geojson.Feature(geometry=point))
    neighbors = geojson.FeatureCollection(neighbors)

    return neighbors


@app.route('/mabr', methods=["GET"])
def mabr():
    """ Description: finds all points within a rectangular area
    Params:
        left: (float) longitude for southwestern-most point
        bottom: (float) latitude for southwestern-most point
        right: (float) longitude for northeastern-most point
        top: (float) latitude for northeastern-most point

    Example: http://localhost:8080/mabr?left=<lng>&bottom=<lat>&right=<lng>&top=<lat>
    """
    global idx
    global rtreeID
    intersections = []

    left = float(request.args.get('left', None))
    bottom = float(request.args.get('bottom', None))
    right = float(request.args.get('right', None))
    top = float(request.args.get('top', None))

    bbox = (left, bottom, right, top)

    indices = list(idx.intersection(bbox))
    for i in indices:
        intersections.append(rtreeID[i])

    intersections = geojson.FeatureCollection(intersections)

    return intersections


@app.route('/cities', methods=["GET"])
def cities():
    """ Description: returns a list of major cities
        Params:
            city (string): city name

        Example: http://localhost:8080/cities?city=<city name>
    """
    filt = request.args.get('city', None)
    # print(filt)
    if filt:
        results = {}
        for city in CITIES:
            if filt.lower() == city[:len(filt)].lower():
                results[city] = CITIES[city]

    else:
        results = CITIES
    return handle_response(results, params="dict")


@app.route("/distance")
def distance():
    """ Description: returns the distance between two points
        Params:
            lng1 (float): a lng point
            lat1 (float): a lat point
            lng2 (float): a lng point
            lat2 (float): a lat point

        Example: http://localhost:8080/distance?lng1=<point>&lat1=<point>&lng2=<point>&lat2=<point>
    """
    lng1 = float(request.args.get("lng1",None))
    lat1 = float(request.args.get("lat1",None))
    lng2 = float(request.args.get("lng2",None))
    lat2 = float(request.args.get("lat2",None))

    point1 = (lng1,lat1)
    point2 = (lng2,lat2)
    distance = {}
    distance['miles'] = haversine(point1,point2,miles=True)
    return distance
    

#                     $$\                      $$\
#                     \__|                     $$ |
#  $$$$$$\   $$$$$$\  $$\ $$\    $$\ $$$$$$\ $$$$$$\    $$$$$$\
# $$  __$$\ $$  __$$\ $$ |\$$\  $$  |\____$$\\_$$  _|  $$  __$$\
# $$ /  $$ |$$ |  \__|$$ | \$$\$$  / $$$$$$$ | $$ |    $$$$$$$$ |
# $$ |  $$ |$$ |      $$ |  \$$$  / $$  __$$ | $$ |$$\ $$   ____|
# $$$$$$$  |$$ |      $$ |   \$  /  \$$$$$$$ | \$$$$  |\$$$$$$$\
# $$  ____/ \__|      \__|    \_/    \_______|  \____/  \_______|
# $$ |
# $$ |
# \__|

def handle_response(data,params=None,error=None):
    """ handle_response
    """
    success = True

    print(data)
    if data:
        if params=='dict':
            pass
            count = len(data)

        elif not isinstance(data,list):
            data = [data]
        count = len(data)
    else:
        count = 0
        error = "Data variable is empty!"


    result = {"success":success,"count":count,"results":data,"params":params}

    if error:
        success = False

        result['error'] = error

    print(f"DATA TYPE of result is {type(result)}")
    print(f"DATA TYPE of jsonify result {type(jsonify(result))}")
    return jsonify(result)


def formatHelp(route):
    """Gets the __doc__ text from a method and formats it for easier reading
        This is __doc__ text
    """
    help = globals().get(str(route)).__doc__
    if help != None:
        help = help.split("\n")
        clean_help = []
        for i in range(len(help)):
            help[i] = help[i].rstrip()
            if len(help[i]) > 0:
                clean_help.append(help[i])
    else:
        clean_help = "No Help Provided."
    return clean_help


def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def isJson(data):
    """
    Helper method to test if val can be json
    without throwing an actual error.
    """
    try:
        json.loads(data)
        return True
    except ValueError:
        return False


def toGeoJson(data, dtype):
    """formats all data input to valid geojson
    """
    dtype = dtype.lower()

    if dtype == "point":
        collection =[]
        for i in range(0,len(data)):
            point = geojson.Point(data[i])
            collection.append(geojson.Feature(geometry=point))
        collection = geojson.FeatureCollection(collection)
        # pp.pprint(collection) # valid
        return collection

    if dtype == "polygon":
        polygon = geojson.Polygon(data)
        # print(polygon)  # valid
        return polygon

    elif dtype == "linestring":
        linestring = geojson.LineString(data)
        # print(linestring) #valid
        return (linestring)

    elif dtype == "multilinestring":
        mls = geojson.MultiLineString(data)
        # print(mls) # valid
        return mls

    else:
        print("\nBAD ARGUMENT\n")




if __name__ == '__main__':

    # {'geometry': {'coordinates': [-111.2224422, 32.436381], 'type': 'Point'}, 'properties': {'marker-color': '#c39953', 'name': 'Marana'}, 'type': 'Feature'}

    tree, coords = getTree()
    idx, rtreeID = getRTree()
    app.run(host='localhost', port=8080,debug=True)



