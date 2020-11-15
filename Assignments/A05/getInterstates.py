import json
from haversine import haversine, Unit

with open("Assignments/A05/Data/grouped_roads.geojson", 'r') as f:
    data= json.load(f)

jsonList =[]
lonList = []
latList = []
id = 0

for feature in data["features"]:
    length = 0
    if feature["properties"]["RTTYP"][0] == "I":
        
        # append lons and lats to parallel lists
        for coords in feature["geometry"]["coordinates"][0]:
            lonList.append(coords[0])
            latList.append(coords[1])
            # print (f"coord:{coords}")

        # make sure lists are the same size
        if len(lonList) == len(latList):

            # get the haversine distance between each set of coords. The sum of all distances is the distance of the entire line
            for i in range(len(lonList)):
                # haversine requires lat,lon tuples
                coord1 = (latList[i], lonList[i])
                coord2 = (latList[(i+1) % len(lonList)], lonList[(i+1) % len(lonList)])
                dist = haversine(coord1, coord2, unit = "mi") # distance in miles
                length += dist
                # input(f"dist {i}: {dist}\n length {i}: {length}")

        # cleanup and assign each line a unique id
        feature["properties"]["RTTYP"] = "I"
        feature["properties"]["LINEARID"] = id
        feature["properties"]["MTFCC"] = feature["properties"]["MTFCC"][0]
        feature["properties"]["LENGTH"] = length
        id += 1

        jsonList.append(feature)
    

# not proud of this but I'm doing it anyway
for interFeature in jsonList:
    for interCoords in interFeature['geometry']['coordinates']:
        for otherFeature in data["features"]:
            for otherCoords in otherFeature["geometry"]["coordinates"][0]:
                if otherCoords not in interCoords:
                    otherFeature["properties"]["RTTYP"] = otherFeature["properties"]["RTTYP"][0]
                    otherFeature["properties"]["LINEARID"] = id
                    otherFeature["properties"]["MTFCC"] = otherFeature["properties"]["MTFCC"][0]
                    id += 1
                    jsonList.append(otherFeature)
  
        




featureCollection = {"type": "FeatureCollection", "features": jsonList}

j = json.dumps(featureCollection)
with open("Assignments/A05/Data/grouped_roads2.geojson", 'w+') as f:
    f.write(j)

j = json.dumps(jsonList, indent = 4)
with open("Assignments/A05/Data/pretty_grouped_roads2.geojson", 'w+') as f:
    f.write(j)





# {
#     "type": "FeatureCollection",
#     "features": [
#         {
#             "type": "Feature",
#             "properties": {
#                 "LINEARID": [
#                     "1105647111403"
#                 ],
#                 "FULLNAME": "morganbranchdr",
#                 "RTTYP": [
#                     "M"
#                 ],
#                 "MTFCC": [
#                     "S1100"
#                 ]
#             },
#             "geometry": {
#                 "type": "MultiLineString",
#                 "coordinates": [
#                     [
#                         [
#                             -75.615623,
#                             38.625174
#                         ],
#                         [
#                             -75.614706,
#                             38.62549
#                         ],
#                         [
#                             -75.610675,
#                             38.62546
#                         ]
#                     ]
#                 ]
#             }
#         }
#     ]
# }