## A03 - Flask Spatial API
### Ben Diekhoff
### Description:
This assignment uses a flask backend and a javascript/html frontend. I have a geojson file full of random lat/lon coordinates that I load into a KDtree.
I use the KDtree to find the nearest neighbors and display the five closest points to the location that the user clicks on the map. 
The radius for nearest neighbors is set to five degrees of lon/lat. Right now clicking on a location prints the lon/lat locations of the five nearest neighbors 
to the console in addition to their distance (in degress) from the original location. They nearest neighbors appear as blue rocket ships on the map. **Users must hit the spacebar to clear the existing neighbors before they click another location on the map!**



### Files
|   #   | File            | Description                                        |
| :---: | --------------- | -------------------------------------------------- |
|   1   | a03.py     | Back end of my project that launches Flask.     |
|   2   | map.html      | Front end of my project. Renders the map.         |
|   3   | templates (folder) | Contains map.html |
|   4   | lonlat.geojson  | Random longitude and latitute coordinates in geojson format             


### Dependencies < Ubuntu >
 1. geojson
 2. json
 3. flask
 4. flask_cors
 5. os,sys
 6. scipy
 

### Instructions
- Create a virtual environment if you dont have one. I used Anaconda
- Install the dependencies above (This is MUCH easier on Linux systems)
- Clone the repository
- From inside `/5443-Spatial-DS-Diekhoff`, open terminal and activate your conda environment
- type `python Assignments/A03/a03.py`
- Hold CTRL and click on the link `http://localhost:8080/'
- Click a location on the map. The lon,lat coordinates from the nearest neighbors will be listed, and the neighbors will appear on the map
- Icons CAN overlap, so you may need to zoom in to see all five
- Press spacebar to clear the current neighbors so you can click somewhere else
- This can be finnicky on Windows! If markers don't appear or appear in the wrong place, try zooming in, hitting spacebar, and clicking again


