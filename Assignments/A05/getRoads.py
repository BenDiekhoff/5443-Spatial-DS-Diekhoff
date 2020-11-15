import json

with open ('Assignments/A05/Data/grouped_Interstates.geojson', 'r') as f:
    inter = json.load(f)

with open ('Assignments/A05/Data/grouped_roads.geojson', 'r') as f:
    other = json.load(f)

for feature in inter["features"]
