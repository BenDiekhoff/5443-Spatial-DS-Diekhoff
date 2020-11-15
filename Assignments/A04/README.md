*Make sure you create a file at /Assignments/A04 called mapboxToken.txt and paste your own token in it*
# Assignment 4 - Visualizing Spatial Data
This assignment uses the Mapbox API and the [Portmap repository](https://github.com/portofportlandgis/portmap) to visualize different data sets and search for spatial data by implementing KDtrees and Rtrees. It uses html and javascript to handle front end stuff and a flask API in python to manage the backend.

# Python Dependencies
- csv
- glob
- json
- os
- sys
- geojson
- rtree
- scipy.spatial (for KDTree)
- flask
- misc functions (included in this repo)

# Features
## Toggleable Layers
- Railroads
- Major Cities
- Earthquakes
- Cell Towers
- Major Rivers
- Oceans
- Populated Places
- Countries
- Mr. Octo and Mr. Claw

## Location Tools
- Put a point on the map by entering lng/lat coordinates
- Remove the point by clicking the clear button
- Click on the map to display the lng/lat of that location

## Draw a Line Between Cities
- Select two cities by typing in the text box (recommendations appear based on what you type)
- The lng/lat coordinates for both cities is displayed upon selection
- Click the Draw Line button to make a green line appear between the cities
- Distance between cities is displayed in miles and kilometers

## Minimum Area Bounding Rectangle
- Click two points on the map (representing the diagonal corners of a rectangle) and a bounding box appears
- All UFO sightings in the bounding box (at least all the one based on my geojson file)are displayed
- This is implemented with an Rtree

## Text
- Paste any valid Feature Collection (Points) in the text box to make the points appear on the map

## Nearest Neighbor
- Enter lng lat coordinates and the number of nearest neighbors to find and the nearest n UFO sightings will be displayed
- This is implemented with a KDTree

## State Bounding Box
- Select a state by typing in a text box (with suggestions)
- A bounding box appears around the selected state

```
# Files (Not all are included, especially compressed files and the Data folder
C:.
│   Data.rar
│   mapboxToken.txt
│   README.md
│   test.txt
│
├───Data
│   │   cellular.geojson
│   │   easyRRS.geojson
│   │   fixed_ufos.geojson
│   │   major_cities.geojson
│   │   mapPoints.geojson
│   │   military_bases.geojson
│   │   states.json
│   │   ufos.geojson
│   │   us_railroads.geojson
│   │   us_railroads_with_states.geojson
│   │   US_State_Bounding_Boxes.csv
│   │   World_Cities.geojson
│   │
│   │
│   ├───earthquake_data ( too long to list)
│
└───portmap
    │   favicon.png
    │   index.html
    │   indexme.html
    │   index_backup.html
    │   index_tutorial.html
    │   LICENSE
    │   README.md
    │   redirect.html
    │
    └───assets
        ├───api
        │   │   flask_api.py
        │   │   flask_api_tutorial.py
        │   │   misc_functions.py
        │   │   tempCodeRunnerFile.py
        │   │
        │   └───__pycache__
        │           misc_functions.cpython-37.pyc
        │
        ├───bootstrap
        │       bootstrap.js
        │       bootstrap.min.js
        │
        ├───css
        │       bootstrap-custom.css
        │       bootstrap.css
        │       bootstrap.min.css
        │       mapbox-gl-custom.css
        │       styles-custom.css
        │       text-editor-style.css
        │
        ├───images
        │       layer-stack-15.svg
        │
        ├───jquery-ui
        │   │   index.html
        │   │   jquery-ui.css
        │   │   jquery-ui.js
        │   │   jquery-ui.min.css
        │   │   jquery-ui.min.js
        │   │   jquery-ui.structure.css
        │   │   jquery-ui.structure.min.css
        │   │   jquery-ui.theme.css
        │   │   jquery-ui.theme.min.css
        │   │
        │   ├───external
        │   │   └───jquery
        │   │           jquery.js
        │   │
        │   └───images
        │           Thumbs.db
        │           ui-bg_flat_0_aaaaaa_40x100.png
        │           ui-bg_flat_75_ffffff_40x100.png
        │           ui-bg_glass_55_fbf9ee_1x400.png
        │           ui-bg_glass_65_ffffff_1x400.png
        │           ui-bg_glass_75_dadada_1x400.png
        │           ui-bg_glass_75_e6e6e6_1x400.png
        │           ui-bg_glass_95_fef1ec_1x400.png
        │           ui-bg_highlight-soft_75_cccccc_1x100.png
        │           ui-icons_222222_256x240.png
        │           ui-icons_2e83ff_256x240.png
        │           ui-icons_454545_256x240.png
        │           ui-icons_888888_256x240.png
        │           ui-icons_cd0a0a_256x240.png
        │
        ├───js
        │       jquery.js
        │       jquery.min.js
        │       map.js
        │       mapREAL.js
        │       print.js
        │
        ├───json
        │       eyes.json
        │       eyes2.json
        │       monster.json
        │       mouth.json
        │       mouth2.json
        │       octo.json
        │       water.json
        │       water2.json
        │
        ├───leaflet
        │       leaflet.js
        │
        └───plugins
            ├───jsonSearch
            │   │   layers.js
            │   │   layerSearch.js
            │   │
            │   ├───chosen
            │   │   │   bower.json
            │   │   │   chosen-sprite.png
            │   │   │   chosen-sprite@2x.png
            │   │   │   chosen.css
            │   │   │   chosen.jquery.js
            │   │   │   chosen.jquery.min.js
            │   │   │   chosen.min.css
            │   │   │   chosen.proto.js
            │   │   │   chosen.proto.min.js
            │   │   │   index.html
            │   │   │   index.proto.html
            │   │   │   options.html
            │   │   │   package.json
            │   │   │
            │   │   └───docsupport
            │   │           chosen.png
            │   │           event.simulate.js
            │   │           oss-credit.png
            │   │           prism.css
            │   │           prism.js
            │   │           style.css
            │   │           Thumbs.db
            │   │
            │   └───json
            │           layers.json
            │
            ├───layerTree
            │   │   gulpfile.js
            │   │   index.html
            │   │   LICENSE
            │   │   package.json
            │   │   README.md
            │   │   yarn.lock
            │   │
            │   ├───css
            │   │       app.css
            │   │       layer-tree.css
            │   │
            │   ├───dist
            │   │   ├───css
            │   │   │       layer-tree-group-settings.css
            │   │   │       styles.min.css
            │   │   │
            │   │   └───js
            │   │           scripts.min - Copy.js.backup
            │   │           scripts.min.js
            │   │           scripts.min.js.backup
            │   │
            │   ├───font-awesome
            │   │   ├───css
            │   │   │       font-awesome.css
            │   │   │       font-awesome.min.css
            │   │   │
            │   │   ├───fonts
            │   │   │       fontawesome-webfont.eot
            │   │   │       fontawesome-webfont.svg
            │   │   │       fontawesome-webfont.ttf
            │   │   │       fontawesome-webfont.woff
            │   │   │       FontAwesome.otf
            │   │   │
            │   │   ├───less
            │   │   │       bordered-pulled.less
            │   │   │       core.less
            │   │   │       fixed-width.less
            │   │   │       font-awesome.less
            │   │   │       icons.less
            │   │   │       larger.less
            │   │   │       list.less
            │   │   │       mixins.less
            │   │   │       path.less
            │   │   │       rotated-flipped.less
            │   │   │       spinning.less
            │   │   │       stacked.less
            │   │   │       variables.less
            │   │   │
            │   │   └───scss
            │   │           font-awesome.scss
            │   │           _bordered-pulled.scss
            │   │           _core.scss
            │   │           _fixed-width.scss
            │   │           _icons.scss
            │   │           _larger.scss
            │   │           _list.scss
            │   │           _mixins.scss
            │   │           _path.scss
            │   │           _rotated-flipped.scss
            │   │           _spinning.scss
            │   │           _stacked.scss
            │   │           _variables.scss
            │   │
            │   ├───icons
            │   │       airplane.svg
            │   │
            │   └───js
            │       │   app.js
            │       │   layer-tree - Copy.js.backup-pre-click
            │       │   layer-tree.js
            │       │   layer-tree.js.20170821
            │       │   layer-tree.js.backup
            │       │
            │       └───jquery-ui-sortable
            │           │   AUTHORS.txt
            │           │   index.html
            │           │   jquery-ui.css
            │           │   jquery-ui.js
            │           │   jquery-ui.min.css
            │           │   jquery-ui.min.js
            │           │   jquery-ui.structure.css
            │           │   jquery-ui.structure.min.css
            │           │   LICENSE.txt
            │           │   package.json
            │           │
            │           └───external
            │               └───jquery
            │                       jquery.js
            │
            └───print-export
                │   gulpfile.js
                │   index.html
                │   land.svg
                │   LICENSE
                │   north_arrow.svg
                │   package.json
                │   README.md
                │   yarn.lock
                │
                ├───css
                │       app.css
                │
                ├───dist
                │   ├───css
                │   │       styles.min.css
                │   │
                │   └───js
                │           scripts.min.js
                │
                ├───js
                │       app.js
                │       print - Copy.js
                │       print.js
                │
                └───libs
                        canvas-to-blob.min.js
                        cropper.min.js
                        FileSaver.min.js
                        html2canvas.min.js
                        jspdf.min.js
                        pdf.combined.min.js
```
