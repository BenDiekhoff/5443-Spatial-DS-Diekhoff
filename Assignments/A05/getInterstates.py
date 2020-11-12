import json
count = 0
with open("Assignments/A05/Data/grouped_roads.geojson", 'r') as f:
    data= json.load(f)


jsonList =[]
for feature in data["features"]:
    # print(feature)
    for properties in feature["properties"]:
        # input(type(properties))
        if feature["properties"]["RTTYP"][0] == "I":
            # input("press enter")
            feature["properties"]["RTTYP"] = "I"
            jsonList.append(feature)
            # print("\n\n\n")
            # print(feature)

j = json.dumps(jsonList)
# j = json.dumps(jsonList, indent = 4)


with open("Assignments/A05/Data/pretty_grouped_Interstates.geojson", 'w+') as f:
    f.write(j)

# print(count)

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