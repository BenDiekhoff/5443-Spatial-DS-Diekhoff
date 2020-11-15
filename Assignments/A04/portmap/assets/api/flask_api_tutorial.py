#!/usr/bin/env python3
import csv
import glob
import json
import os
import sys

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

base_path = 'Assignments/A04/Data'

def load_data(path):
    """Given a path, load the file and handle it based on its extension type. 
    """

    _, ftype = os.path.splitext(path) #get fname and extension

    if os.path.isfile(path):
        with open(path) as f:

            if ftype == ".json" or ftype == ".geojson":    #handle json
                data = json.load(f)
                # print(data)
                return data

            elif ftype == ".csv":   #handle csv with csv reader
                with open(path, newline ='') as csvfile:
                    data = csv.DictReader(csvfile)
                    return list(data)

            else:
                print("neither json or csv")
                return None

# STATES = load_data('Assignments/A04/Data/countries_states/states.json')
# STATE_BBOXS = load_data('Assignments/A04/Data/US_State_Bounding_Boxes.csv')




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
    with open ('Assignments/A04/mapboxToken.txt', 'r') as f:
        mapbox_access_token = f.read()

    return mapbox_access_token


@app.route("/", methods=["GET"])
def getRoutes():
    """ getRoutes: this gets all the routes!
    """
    routes = {}
    for r in app.url_map._rules:
        # print(r)
        routes[r.rule] = {}
        routes[r.rule]["functionName"] = r.endpoint
        routes[r.rule]["help"] = formatHelp(r.endpoint)
        routes[r.rule]["methods"] = list(r.methods)

    routes.pop("/static/<path:filename>")
    routes.pop("/")

    response = json.dumps(routes,indent=4,sort_keys=True)
    response = response.replace("\n","<br>")
    return "<pre>"+response+"</pre>"

@app.route('/neighbor', methods = ["GET"])
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
    lon = float(request.args.get('lon',None))
    lat = float(request.args.get('lat',None))
    num = int(request.args.get('num',None))

    searchCoords=[lon,lat]     #[[98.581081, 29.38421],[98.581081, 29.38421]]
    # returns an array of distances and an array of indices for nearest neighbors
    distanceList, neighborList = tree.query(searchCoords,k=num,distance_upper_bound=180)
    print(type(neighborList))

    # prints the results of the query to the console
    if num > 1:
        for i in range(0,num):
            print(f"\nLng, Lat: {lon}, {lat}\nNearest neighbor: {coords[neighborList[i]]}\tDistance: {distanceList[i]}")
    else:
        print(f"\nLng, Lat: {lon}, {lat}\nNearest neighbor: {neighborList}\tDistance: {distanceList}")

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





#                                                         $$\     
#                                                         $$ |    
#  $$$$$$\   $$$$$$\   $$$$$$\  $$\  $$$$$$\   $$$$$$$\ $$$$$$\   
# $$  __$$\ $$  __$$\ $$  __$$\ \__|$$  __$$\ $$  _____|\_$$  _|  
# $$ /  $$ |$$ |  \__|$$ /  $$ |$$\ $$$$$$$$ |$$ /        $$ |    
# $$ |  $$ |$$ |      $$ |  $$ |$$ |$$   ____|$$ |        $$ |$$\ 
# $$$$$$$  |$$ |      \$$$$$$  |$$ |\$$$$$$$\ \$$$$$$$\   \$$$$  |
# $$  ____/ \__|       \______/ $$ | \_______| \_______|   \____/ 
# $$ |                    $$\   $$ |                              
# $$ |                    \$$$$$$  |                              
# \__|                     \______/                               



# @app.route('/states', methods=["GET"])
# def states():
#     """ Description: return menu for front end
#         Params: 
#             None
#         Example: http://localhost:8080/states?filter=mis
#     """
#     filt = request.args.get('filter',None)
#     # print(filt)
#     if filt:
#         results = []
#         for state in STATES:
#             if filt.lower() == state['name'][:len(filt)].lower():
#                 results.append(state)
#     else:
#         results = STATES

#     return handle_response(results)





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
    if data:
        if not isinstance(data,list):
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
    print(f"DATA TYPE of jsonify result {type(jsonify(result_))}")
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

if __name__ == '__main__':
      app.run(host='localhost', port=8080,debug=True)