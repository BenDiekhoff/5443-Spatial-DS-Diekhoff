mapboxgl.accessToken = 'pk.eyJ1IjoiYmVuZGlla2hvZmYiLCJhIjoiY2sxcGp5bWlxMGNwbjNibGZ1cW9seDd2aSJ9.cPovo_u9sG8eOqRSCw_Cew';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-69.0297, 7.61],
    zoom: 2,
    attributionControl: true,
    preserveDrawingBuffer: true,
});

// handles click/touch event across devices 
let touchEvent = 'ontouchstart' in window ? 'touchstart' : 'click';

// navigation controls
map.addControl(new mapboxgl.NavigationControl()); // zoom controls

// scale bar
map.addControl(new mapboxgl.ScaleControl({
    maxWidth: 90,
    unit: 'imperial',
    position: 'bottom-right'
}));

// geolocate control
map.addControl(new mapboxgl.GeolocateControl());

//This overides the Bootstrap modal "enforceFocus" to allow user interaction with main map
$.fn.modal.Constructor.prototype.enforceFocus = function () { };

// print function
var printBtn = document.getElementById('mapboxgl-ctrl-print');
var exportView = document.getElementById('export-map');

var printOptions = {
    disclaimer: "print output disclaimer",
    northArrow: 'assets/plugins/print-export/north_arrow.svg'
}

printBtn.onclick = function (e) {
    PrintControl.prototype.initialize(map, printOptions)
}

exportView.onclick = function (e) {
    PrintControl.prototype.exportMap();
    e.preventDefault();
}


// Layer Search Event Handlers
$('#search_general').on('click', function (e) {

    var criteria = $('#general_search').val();
    var prop = $('#property-descr').text();
    var layer_mapfile = $('#json_layer').val();

    addJsonLayerFilter(layer_mapfile, prop, criteria);

});

$('#clear_general').on('click', function (e) {

    $("#general_search").val("");
    $("#property-descr").html("<br />");
    clearFilterLayer();

});

// Geocoder API
// Geocoder API
// Geocoder API
var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken
});

var addressTool = document.getElementById('addressAppend');
addressTool.appendChild(geocoder.onAdd(map))

map.on('load', function () {
    map.addSource('geocode-point', {
        "type": "geojson",
        "data": {
            "type": "FeatureCollection",
            "features": []
        }
    });

    map.addLayer({
        "id": "geocode-point",
        "source": "geocode-point",
        "type": "circle",
        "paint": {
            "circle-radius": 20,
            "circle-color": "dodgerblue",
            'circle-opacity': 0.5,
            'circle-stroke-color': 'white',
            'circle-stroke-width': 3,
        }
    });

    geocoder.on('result', function (ev) {
        map.getSource('geocode-point').setData(ev.result.geometry);
    });

});
//creating a new layer ? to se
//if i can use it to upload points-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -
map.on('load', function() {
    //DataSets layer
    map.addSource('ufo', { type: 'geojson', data: emptyGJ });
    map.addLayer({
        "id": "ufo",
        "type": "circle",
        "source": "ufo",
        "layout": {
            "visibility": 'none'
        },
        "paint": {
            "circle-color": 'green',
            "circle-radius": 8
        }
    });
    map.addSource('railroads', { type: 'geojson', data: emptyGJ });
    map.addLayer({
        "id": "railroads",
        "type": "circle",
        "source": "railroads",
        "layout": {
            "visibility": 'none'
        },
        "paint": {
            "circle-color": 'purple',
            "circle-radius": 8
        }
    });
    map.addSource('cities', { type: 'geojson', data: emptyGJ });
    map.addLayer({
        "id": "cities",
        "type": "circle",
        "source": "cities",
        "layout": {
            "visibility": 'none'
        },
        "paint": {
            "circle-color": 'orange',
            "circle-radius": 8
        }
    });
})
var layers =
    [{
            'name': 'ufo',
            'id': 'ufo',
            'source': 'ufo',
            'path': 'Assignments/A04/Data/ufo_data/fixed_ufos.geojson',
            'directory': 'Dataset',
        }, {
            'name': 'railroads',
            'id': 'railroads',
            'source': 'railroads',
            'path': 'https://geo.dot.gov/server/rest/services/Hosted/North_American_Rail_Lines_DS/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json', //'/Users/Delly/Desktop/NewEnv/5443-Spatial-DS-Augustine/Assignments/A04/assets/api/data/us_railroads.geojson',
            'directory': 'Dataset',
        },
        {
            'name': 'cities',
            'id': 'cities',
            'source': 'cities',
            'path': 'Assignments/A04/Data/countries_states/major_cities.geojson',
            'directory': 'Dataset',
        }
    ];
map.addControl(new LayerTree({
    layers: layers,
    onClickLoad: true
}), 'bottom-left');
var emptyGJ = {
    'type': 'FeatureCollection',
    'features': []
};
/convert marker DOM elements to symbol layers
function markerToSymbol(e, elm) {
    if (isDragging) return;
    MAP_DIV.style.cursor = '';
    var that = this instanceof Element ? this : elm;
    var childSpan = document.querySelector('.marker-text-child');
    if (childSpan) var parent = childSpan.parentNode;
    if (that.innerText !== '' && that.innerText.length > 0) {
        parent ? parent.classList.remove('active') : that.classList.remove('active');
        var fontSize = that.style['font-size'] === '' ? TEXT_SIZES[1] : parseInt(that.style['font-size'].split('px')[0]); //textSize[1] is default
        var fontColor = that.style.color === '' ? '#000' : that.style.color;
        var coords = [that.getAttribute('lng'), that.getAttribute('lat')];
        var labelGJ = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Point",
                    "coordinates": coords
                }
            }]
        };
        var id = generateTextID();
        var lyrID = id + '-custom-text-label';
        map.addSource(id, { type: 'geojson', data: labelGJ });
        map.addLayer({
            "id": lyrID,
            "type": "symbol",
            "source": id,
            "layout": {
                "text-field": that.innerText,
                "text-size": fontSize,
                "symbol-placement": "point",
                "text-keep-upright": true
            },
            "paint": {
                "text-color": fontColor,
                "text-halo-color": '#FFF',
                "text-halo-width": 2,
            },
        });
        //removes text-input marker after clicking off
        LABEL_NODE.setAttribute('active', false);
        that.removeEventListener('blur', markerToSymbol);
    }
    parent ? parent.remove() : that.remove();
}
//label text limit/prevent event keys
function inputText(e) {
    console.log(e.key, e.keyCode)
    //arrow keys
    if ([32, 37, 38, 39, 40, 8].indexOf(e.keyCode) > -1) {
        e.stopPropagation();
        //enter key
    } else if (e.keyCode === 13 && this.innerText.length <= CHAR_LIMIT) {
        this.blur();
        MAP_DIV.style.cursor = '';
        e.preventDefault();
        //limit
    } else if (this.innerText.length >= CHAR_LIMIT && e.keyCode !== 8) {
        e.preventDefault();
        alert(keycode);
    }
}


//      $$\                                                    $$$$$$$$\                            
//      $$ |                                                   \__$$  __|                           
//      $$ |      $$$$$$\  $$\   $$\  $$$$$$\   $$$$$$\           $$ | $$$$$$\   $$$$$$\   $$$$$$\  
//      $$ |      \____$$\ $$ |  $$ |$$  __$$\ $$  __$$\          $$ |$$  __$$\ $$  __$$\ $$  __$$\ 
//      $$ |      $$$$$$$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|         $$ |$$ |  \__|$$$$$$$$ |$$$$$$$$ |
//      $$ |     $$  __$$ |$$ |  $$ |$$   ____|$$ |               $$ |$$ |      $$   ____|$$   ____|
//      $$$$$$$$\\$$$$$$$ |\$$$$$$$ |\$$$$$$$\ $$ |               $$ |$$ |      \$$$$$$$\ \$$$$$$$\ 
//      \________|\_______| \____$$ | \_______|\__|               \__|\__|       \_______| \_______|
//                         $$\   $$ |                                                               
//                         \$$$$$$  |                                                               
//                          \______/                                                                
// Layer Tree
var emptyGJ = {
    'type': 'FeatureCollection',
    'features': []
};
map.on('load', function () {
    //Load Layers
    // Layers that load first will be at the bottom of the root directory within the Layer Tree



    //UFO layers
    //UFO layers
    map.addSource('ufo', { type: 'geojson', data: emptyGJ });
    map.addLayer({
        "id": "ufo",
        "type": "circle",
        "source": "country",
        "layout": {
            //"visibility": 'none'
        },
        "paint": {
            'fill-color': 'blue',
            'fill-opacity': .5,
            'fill-outline-color': '#333333',
        }
    });







    map.on('load', function () {

        //UFO layers
        //UFO layers
        map.addSource('ufo', { type: 'geojson', data: emptyGJ });
        map.addLayer({
            "id": "ufo",
            "type": "circle",
            "source": "country",
            "layout": {
                //"visibility": 'none'
            },
            "paint": {
                'fill-color': 'blue',
                'fill-opacity': .5,
                'fill-outline-color': '#333333',
            }
       });
     })
     var layers = [
         
    {
        'name': 'ufo',
        'id': 'ufo',
        'source': 'ufo',
        'path': 'C:/Users/Ben-Study/Desktop/5443-Spatial-DS-Diekhoff/Assignments/A04/Data/ufo_data/fixed_ufos.geojson',
        'directory': 'dataSet',
    },
    {
        'name': 'earthquakes',
        'id': 'earthquakes',
        'source': 'earthquakes',
        'path': 'C:/Users/Ben-Study/Desktop/5443-Spatial-DS-Diekhoff/Assignments/A04/Data/earthquake_data/earthquakes/1950_7.json',
        'directory': 'Dataset',
    }
    ];
    map.addControl(new LayerTree({
        layers: layers,
        onClickLoad: true
    }), 'bottom-left');

        //cultural layers
        //cultural layers
        map.addSource('country', { type: 'geojson', data: emptyGJ });
        map.addLayer({
            "id": "country",
            "type": "fill",
            "source": "country",
            "layout": {
                //"visibility": 'none'
            },
            "paint": {
                'fill-color': '#595959',
                'fill-opacity': .5,
                'fill-outline-color': '#333333',
            }
        });


        map.addSource('populated', { type: 'geojson', data: emptyGJ });
        map.addLayer({
            "id": "populated",
            "type": "circle",
            "source": "populated",
            "layout": {
                "visibility": 'none'
            },
            "paint": {
                'circle-color': 'white',
                'circle-opacity': 1.0,
                'circle-stroke-color': '#ff8c1a',
                'circle-stroke-width': 2,
                'circle-stroke-opacity': 1.0,
            }
        });


        //physical layers
        //physical layers
        map.addSource('ocean', { type: 'geojson', data: emptyGJ });
        map.addLayer({
            "id": "ocean",
            "type": "fill",
            "source": "ocean",
            "layout": {
                "visibility": 'none'
            },
            "paint": {
                'fill-color': '#00334d',
                'fill-opacity': 0.5,
                'fill-outline-color': '#00111a',
            }
        });

        map.addSource('river', { type: 'geojson', data: emptyGJ });
        map.addLayer({
            "id": "river",
            "type": "line",
            "source": "river",
            "layout": {
                "visibility": 'none'
            },
            "paint": {
                'line-color': '#0099cc',
                'line-opacity': .8,
                "line-width": 4,
            },
        });



        //Layer Info function
        //Layer Info function
        //Layer Info function
        //Layer Info function
        map.on(touchEvent, function (e) {

            document.getElementById("layer-attribute").innerHTML = "";

        });

        map.on(touchEvent, function (e) {

            var popup = new mapboxgl.Popup();
            var feature;
            var append = document.getElementById('layer-attribute');

            //Cultural - Layer Info
            //Cultural - Layer Info

            if (map.queryRenderedFeatures(e.point, { layers: ['populated'] }).length) {

                feature = map.queryRenderedFeatures(e.point, { layers: ['populated'] })[0];

                append.innerHTML +=
                    '<h5>Populated Places</h5>' +
                    '<hr>' +
                    '<b>City: </b>' + feature.properties.name +
                    '<hr>' +
                    '<b>Country: </b>' + feature.properties.sov0name +
                    '<hr>'
            }

            if (map.queryRenderedFeatures(e.point, { layers: ['country'] }).length) {

                feature = map.queryRenderedFeatures(e.point, { layers: ['country'] })[0];

                append.innerHTML +=
                    '<h5>Country</h5>' +
                    '<hr>' +
                    '<b>Port Name </b>' + feature.properties.admin +
                    '<hr>' +
                    '<b>Code: </b>' + feature.properties.adm0_a3 +
                    '<hr>'
            }


            //Physical - Layer Info
            //Physical  - Layer Info
            if (map.queryRenderedFeatures(e.point, { layers: ['ocean'] }).length) {

                feature = map.queryRenderedFeatures(e.point, { layers: ['ocean'] })[0];

                append.innerHTML +=
                    '<h5>Oceans</h5>' +
                    '<hr>' +
                    '<b>Name: </b>' + feature.properties.name +
                    '<hr>'
            }

            if (map.queryRenderedFeatures(e.point, { layers: ['river'] }).length) {

                feature = map.queryRenderedFeatures(e.point, { layers: ['river'] })[0];

                append.innerHTML +=
                    '<h5>Major Rivers</h5>' +
                    '<hr>' +
                    '<b>Name: </b>' + feature.properties.name +
                    '<hr>'
            }
        });

        //cursor = pointer on hover configuration
        map.on('mousemove', function (e) {
            var features = map.queryRenderedFeatures(e.point, {
                layers: ['ocean', 'river', 'country', 'populated']//, 'monster', 'octo']
            });
            map.getCanvas().style.cursor = (features.length) ? 'default' : '';
        });

        //Highlight Features Function
        //Highlight Features Function
        //Highlight Features Function
        //Highlight Features Function
        map.on(touchEvent, function (e) {
            var features = map.queryRenderedFeatures(e.point, { layers: ["populated"] });

            if (map.getLayer("populated_hl")) {
                map.removeLayer("populated_hl");
            }

            if (features.length) {

                map.addLayer({
                    "id": "populated_hl",
                    "type": "circle",
                    "source": "populated",
                    "layout": {},
                    "paint": {
                        "circle-color": "cyan",
                        "circle-radius": 7
                    },
                    "filter": ["==", "name", features[0].properties.name],
                });
            }
        });

        map.on(touchEvent, function (e) {
            var features = map.queryRenderedFeatures(e.point, { layers: ["country"] });

            if (map.getLayer("country_hl")) {
                map.removeLayer("country_hl");
            }

            if (features.length) {

                map.addLayer({
                    "id": "country_hl",
                    "type": "line",
                    "source": "country",
                    "layout": {},
                    "paint": {
                        "line-color": "cyan",
                        "line-width": 3
                    },
                    "filter": ["==", "sovereignt", features[0].properties.sovereignt],
                });
            }
        });



        //Highlight - Physical
        map.on(touchEvent, function (e) {
            var features = map.queryRenderedFeatures(e.point, { layers: ["river"] });

            if (map.getLayer("river_hl")) {
                map.removeLayer("river_hl");
            }

            if (features.length) {

                map.addLayer({
                    "id": "river_hl",
                    "type": "line",
                    "source": "river",
                    "layout": {},
                    "paint": {
                        "line-color": "cyan",
                        "line-width": 4
                    },
                    "filter": ["==", "name", features[0].properties.name],
                });
            }
        });

        map.on(touchEvent, function (e) {
            var features = map.queryRenderedFeatures(e.point, { layers: ["ocean"] });

            if (map.getLayer("ocean_hl")) {
                map.removeLayer("ocean_hl");
            }

            if (features.length) {

                map.addLayer({
                    "id": "ocean_hl",
                    "type": "line",
                    "source": "ocean",
                    "layout": {},
                    "paint": {
                        "line-color": "cyan",
                        "line-width": 3
                    },
                    "filter": ["==", "name", features[0].properties.name],
                });
            }
        });
    });

    // Directory Options
    // Directory Options
    // Directory Options - open or closed by defualt (true/false)
    var directoryOptions =
        [
            {
                'name': 'dataSet',
                'open': true
            },
            {
                'name': 'Monsters',
                'open': true
            },
            {
                'name': 'Cultural',
                'open': true
            },
            {
                'name': 'Physical',
                'open': true
            },

        ];

    // organize layers in the layer tree
    var layers =

        [
            {
                'name': 'Populated Places',
                'id': 'populated',
                'source': "populated",
                'path': 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_populated_places_simple.geojson',
                'directory': 'Cultural',
            },
            {
                'name': 'Countries',
                'id': 'country',
                'source': 'country',
                'path': 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_0_map_units.geojson',
                'directory': 'Cultural',
            },


            // Physical LAYER TREE CONFIG
            // Physical LAYER TREE CONFIG

            {
                'name': 'Major Rivers',
                'id': 'river',
                'source': 'river',
                'path': 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_rivers_lake_centerlines.geojson',
                'directory': 'Physical',
            },
            {
                'name': 'Oceans',
                'id': 'ocean',
                'source': 'ocean',
                'path': '',
                'directory': 'dataSet',
            },

        ];


    var layerList = new LayerTree({ layers: layers, directoryOptions: directoryOptions, onClickLoad: true });

    var layerTool = document.getElementById('menu');
    layerTool.appendChild(layerList.onAdd(map))


    //BOOKMARKS
    //BOOKMARKS
    //BOOKMARKS

    document.getElementById('icelandBookmark').addEventListener('click', function () {

        map.flyTo({
            center: [-18.7457, 65.0662],
            zoom: 5,
        });
    });

    document.getElementById('safricaBookmark').addEventListener('click', function () {

        map.flyTo({
            center: [23.9417, -29.5353],
            zoom: 5,
        });
    });

    document.getElementById('japanBookmark').addEventListener('click', function () {

        map.flyTo({
            center: [138.6098, 36.3223],
            zoom: 4,
        });
    });

    document.getElementById('australiaBookmark').addEventListener('click', function () {

        map.flyTo({
            center: [134.1673, -25.6855],
            zoom: 3

        });
    });



    //TEXT TOOL
    //TEXT TOOL
    //TEXT TOOL

    var MAP_DIV = map.getCanvasContainer();
    var EDIT_NODE = document.getElementById('editTextTool');
    var LABEL_NODE = document.getElementById('textTool');

    //set user defined sizes/colors in palette
    var TEXT_SIZES = [24, 20, 16, 12];
    var TEXT_COLORS = ['#000', '#c12123', '#ee4498', '#00924d', '#00afde', '#ccbe00'];

    //char count limit
    var CHAR_LIMIT = 20;

    //drag status
    var isDragging = false;


    function activateTool(el) {
        if (el.getAttribute('active') === 'true') {
            el.setAttribute('active', false);

            if (el.isEqualNode(EDIT_NODE)) {
                var activeInput = document.querySelector('.label-marker.active span');
                if (activeInput) {
                    activeInput.focus();
                    activeInput.blur();
                }
            }
            MAP_DIV.style.cursor = '';

        } else {
            el.isEqualNode(EDIT_NODE) ? LABEL_NODE.setAttribute('active', false) : EDIT_NODE.setAttribute('active', false);
            el.setAttribute('active', true);

            MAP_DIV.style.cursor = 'crosshair';
        }
    }

    //generate unique layer ids for text-labels
    function generateTextID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    //convert marker DOM elements to symbol layers
    function markerToSymbol(e, elm) {
        if (isDragging) return;

        MAP_DIV.style.cursor = '';

        var that = this instanceof Element ? this : elm;
        var childSpan = document.querySelector('.marker-text-child');

        if (childSpan) var parent = childSpan.parentNode;

        if (that.innerText !== '' && that.innerText.length > 0) {
            parent ? parent.classList.remove('active') : that.classList.remove('active');

            var fontSize = that.style['font-size'] === '' ? TEXT_SIZES[1] : parseInt(that.style['font-size'].split('px')[0]); //textSize[1] is default
            var fontColor = that.style.color === '' ? '#000' : that.style.color;
            var coords = [that.getAttribute('lng'), that.getAttribute('lat')];

            var labelGJ = {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {},
                        "geometry": {
                            "type": "Point",
                            "coordinates": coords
                        }
                    }
                ]
            };

            var id = generateTextID();
            var lyrID = id + '-custom-text-label';

            map.addSource(id, { type: 'geojson', data: labelGJ });

            map.addLayer({
                "id": lyrID,
                "type": "symbol",
                "source": id,
                "layout": {
                    "text-field": that.innerText,
                    "text-size": fontSize,
                    "symbol-placement": "point",
                    "text-keep-upright": true
                },
                "paint": {
                    "text-color": fontColor,
                    "text-halo-color": '#FFF',
                    "text-halo-width": 2,
                },
            });

            //removes text-input marker after clicking off
            LABEL_NODE.setAttribute('active', false);

            that.removeEventListener('blur', markerToSymbol);
        }

        parent ? parent.remove() : that.remove();
    }

    //label text limit/prevent event keys
    function inputText(e) {

        console.log(e.key, e.keyCode)

        //arrow keys
        if ([32, 37, 38, 39, 40, 8].indexOf(e.keyCode) > -1) {
            e.stopPropagation();
            //enter key

        } else if (e.keyCode === 13 && this.innerText.length <= CHAR_LIMIT) {
            this.blur();

            MAP_DIV.style.cursor = '';

            e.preventDefault();
            //limit
        } else if (this.innerText.length >= CHAR_LIMIT && e.keyCode !== 8) {
            e.preventDefault();
            alert(keycode);
        }
    }


    //pasting text into requires additional handling
    //for text limit
    function handlePaste(e) {
        var clipboardData, pastedData;

        e.stopImmediatePropagation();
        e.preventDefault();

        clipboardData = e.clipboardData || window.clipboardData;
        pastedData = clipboardData.getData('text/plain').slice(0, CHAR_LIMIT);

        this.innerText = pastedData;
    }

    function createMarker(e, el) {

        new mapboxgl.Marker(el)
            .setLngLat(e.lngLat)
            .addTo(map);
    }

    //populates edit palette with user defined colors/sizes
    function populatePalette() {
        var palette = document.getElementById('customTextPalette');
        var textSizeDiv = document.getElementById('customTextSize');
        var textColorDiv = document.getElementById('customTextColor');

        for (var s = 0; s < TEXT_SIZES.length; s++) {
            var sElm = document.createElement('div');
            sElm.className = 'font-size-change';
            sElm.id = 'font-' + TEXT_SIZES[s];
            sElm.innerText = 'T'; //change to whatever font/image
            sElm.style['font-size'] = TEXT_SIZES[s] + 'px';
            sElm.addEventListener('mousedown', changeFontStyle);

            textSizeDiv.appendChild(sElm);
        };

        for (var c = 0; c < TEXT_COLORS.length; c++) {
            var cElm = document.createElement('div');
            cElm.className = 'font-color-change';
            cElm.id = 'font-' + TEXT_COLORS[c];
            cElm.style['background-color'] = TEXT_COLORS[c];
            cElm.addEventListener('mousedown', changeFontStyle);

            textColorDiv.appendChild(cElm);
        };
    }

    //update marker font styles
    function changeFontStyle(e) {
        e.preventDefault();
        e.stopPropagation();

        var labelDiv = document.querySelector('.label-marker');
        var childSpan = document.querySelector('.marker-text-child');

        var mark = childSpan ? childSpan : labelDiv;

        if (mark) {
            labelDiv.classList.add('active');
            if (e.target.classList.contains('font-size-change')) {
                mark.style['font-size'] = e.target.style['font-size'];
            } else if (e.target.classList.contains('font-color-change')) {
                mark.style.color = e.target.style['background-color'];
            }

            mark.focus();
        }

        MAP_DIV.style.cursor = 'text';
    }

    //marker move functionality - modified GL example
    //https://www.mapbox.com/mapbox-gl-js/example/drag-a-point/
    function beginDrag(e) {
        e.stopImmediatePropagation();

        map.dragPan.disable();

        isDragging = true;

        MAP_DIV.style.cursor = 'cursor:-moz-grab;cursor:-webkit-grab;cursor:grab';

        map.on('mousemove', onDrag);
        map.on('touchmove', onDrag);

        map.once('mouseup', stopDrag);
        map.once('touchend', stopDrag);
    }

    function onDrag(e) {
        if (!isDragging) return;

        var label = document.querySelector('.label-marker');

        MAP_DIV.style.cursor = 'cursor:-moz-grabbing;cursor:-webkit-grabbing;cursor:grabbing';

        map.dragPan.disable();

        createMarker(e, label);
    }

    function stopDrag(e) {
        if (!isDragging) return;

        var textSpan = document.querySelector('.marker-text-child');

        textSpan.setAttribute('lng', e.lngLat.lng);
        textSpan.setAttribute('lat', e.lngLat.lat);

        isDragging = false;

        textSpan.parentNode.style.cursor = '';
        MAP_DIV.style.cursor = '';

        map.dragPan.enable();

        setTimeout(function () {
            markerToSymbol(e, textSpan);
        }, 50)

        // Unbind move events
        map.off('mousemove', onDrag);
        map.off('touchmove', onDrag);
    }

    function addEditLabels(e) {
        e.originalEvent.preventDefault();
        e.originalEvent.stopPropagation();

        if (isDragging) return;

        //create a large bounding box for capture
        var clickBBox = [[e.point.x - 2, e.point.y - 2], [e.point.x + 2, e.point.y + 2]];

        //adding text
        if (LABEL_NODE.getAttribute('active') === 'true') {

            var el = document.createElement('div');
            el.className = 'label-marker';

            el.setAttribute('contenteditable', 'true');
            el.setAttribute('autocorrect', 'off');
            el.setAttribute('spellcheck', 'false');
            el.setAttribute('lng', e.lngLat.lng);
            el.setAttribute('lat', e.lngLat.lat);
            el.style['font-size'] = TEXT_SIZES[1] + 'px';  //defaulting to second size

            map.marker = createMarker(e, el);

            el.addEventListener("blur", markerToSymbol);
            el.addEventListener("keydown", inputText);
            el.addEventListener("paste", handlePaste);

            el.focus();

            //editting text
        } else if (EDIT_NODE.getAttribute('active') === 'true') {

            //filters layers for custom text labels
            function isCustomText(item) {
                return item.layer.id.indexOf('-custom-text-label') > -1
            }

            var features = map.queryRenderedFeatures(clickBBox);
            var activeInput = document.querySelector('.marker-text-child');

            if (features.length) {
                var customLabels = features.filter(isCustomText);

                if (customLabels.length) {
                    //only returning the first feature
                    //user is going to have to zoom in further
                    var feature = customLabels[0].layer;

                    var lyrID = feature.id;
                    var sourceID = feature.source;
                    var text = feature.layout['text-field'];
                    var featureFontSize = feature.layout['text-size'] + 'px';
                    var featureFontColor = feature.paint['text-color'];

                    var mapSource = map.getSource(sourceID);
                    var coords = mapSource._data.features[0].geometry.coordinates;

                    var container = document.createElement('div');
                    container.className = 'label-marker label-container active';

                    var el = document.createElement('span');
                    el.className = 'marker-text-child';
                    el.innerText = text;

                    el.style['font-size'] = featureFontSize;
                    el.style.color = featureFontColor;

                    el.setAttribute('lng', coords[0]);
                    el.setAttribute('lat', coords[1]);
                    el.setAttribute('contenteditable', 'true');
                    el.setAttribute('autocorrect', 'off');
                    el.setAttribute('spellcheck', 'false');

                    //drag icon - using FontAwesome as an example
                    var dragUI = document.createElement('i');
                    dragUI.className = 'fa fa-arrows-alt fa-lg drag-icon';
                    dragUI.setAttribute('aria-hidden', true);

                    container.appendChild(dragUI);
                    container.appendChild(el);

                    map.removeSource(sourceID);
                    map.removeLayer(lyrID);

                    createMarker(e, container);

                    dragUI.addEventListener("mousedown", beginDrag);
                    dragUI.addEventListener("touchstart", beginDrag);

                    el.addEventListener("blur", markerToSymbol);
                    el.addEventListener("keydown", inputText);
                    el.addEventListener("paste", handlePaste);

                } else if (activeInput) {
                    activeInput.isEqualNode(e.originalEvent.target) ? activeInput.focus() : markerToSymbol(e, activeInput);
                }
            }
        }
    }

    //fire function to populate text/color custom pallete
    populatePalette();

    map.on('click', addEditLabels);


    // custom draw styles paramaters
    // custom draw styles paramaters
    // custom draw styles paramaters
    var drawFeatureID = '';
    var newDrawFeature = false;
    var trackDrawnPolygons = [];
    var getLastDrawnPoly = false;

    //Draw Tools function
    //Draw Tools function
    //Draw Tools function
    var draw = new MapboxDraw({
        // this is used to allow for custom properties for styling draw features
        // it appends the word "user_" to the property
        userProperties: true,
        displayControlsDefault: false,
        controls: {
            polygon: true,
            point: true,
            line_string: true,
            trash: true,
        },
        styles: [
            // default themes provided by MB Draw
            // default themes provided by MB Draw
            // default themes provided by MB Draw
            // default themes provided by MB Draw


            {
                'id': 'gl-draw-polygon-fill-inactive',
                'type': 'fill',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Polygon'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'fill-color': '#3bb2d0',
                    'fill-outline-color': '#3bb2d0',
                    'fill-opacity': 0.1
                }
            },
            {
                'id': 'gl-draw-polygon-fill-active',
                'type': 'fill',
                'filter': ['all', ['==', 'active', 'true'],
                    ['==', '$type', 'Polygon']
                ],
                'paint': {
                    'fill-color': '#fbb03b',
                    'fill-outline-color': '#fbb03b',
                    'fill-opacity': 0.1
                }
            },
            {
                'id': 'gl-draw-polygon-midpoint',
                'type': 'circle',
                'filter': ['all', ['==', '$type', 'Point'],
                    ['==', 'meta', 'midpoint']
                ],
                'paint': {
                    'circle-radius': 3,
                    'circle-color': '#fbb03b'
                }
            },
            {
                'id': 'gl-draw-polygon-stroke-inactive',
                'type': 'line',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Polygon'],
                    ['!=', 'mode', 'static']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#3bb2d0',
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-polygon-stroke-active',
                'type': 'line',
                'filter': ['all', ['==', 'active', 'true'],
                    ['==', '$type', 'Polygon']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#fbb03b',
                    'line-dasharray': [0.2, 2],
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-line-inactive',
                'type': 'line',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'LineString'],
                    ['!=', 'mode', 'static']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#3bb2d0',
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-line-active',
                'type': 'line',
                'filter': ['all', ['==', '$type', 'LineString'],
                    ['==', 'active', 'true']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#fbb03b',
                    'line-dasharray': [0.2, 2],
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-polygon-and-line-vertex-stroke-inactive',
                'type': 'circle',
                'filter': ['all', ['==', 'meta', 'vertex'],
                    ['==', '$type', 'Point'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-color': '#fff'
                }
            },
            {
                'id': 'gl-draw-polygon-and-line-vertex-inactive',
                'type': 'circle',
                'filter': ['all', ['==', 'meta', 'vertex'],
                    ['==', '$type', 'Point'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 3,
                    'circle-color': '#fbb03b'
                }
            },
            {
                'id': 'gl-draw-point-point-stroke-inactive',
                'type': 'circle',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Point'],
                    ['==', 'meta', 'feature'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-opacity': 1,
                    'circle-color': '#fff'
                }
            },
            {
                'id': 'gl-draw-point-inactive',
                'type': 'circle',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Point'],
                    ['==', 'meta', 'feature'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 3,
                    'circle-color': '#3bb2d0'
                }
            },
            {
                'id': 'gl-draw-point-stroke-active',
                'type': 'circle',
                'filter': ['all', ['==', '$type', 'Point'],
                    ['==', 'active', 'true'],
                    ['!=', 'meta', 'midpoint']
                ],
                'paint': {
                    'circle-radius': 7,
                    'circle-color': '#fff'
                }
            },
            {
                'id': 'gl-draw-point-active',
                'type': 'circle',
                'filter': ['all', ['==', '$type', 'Point'],
                    ['!=', 'meta', 'midpoint'],
                    ['==', 'active', 'true']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-color': '#fbb03b'
                }
            },
            {
                'id': 'gl-draw-polygon-fill-static',
                'type': 'fill',
                'filter': ['all', ['==', 'mode', 'static'],
                    ['==', '$type', 'Polygon']
                ],
                'paint': {
                    'fill-color': '#404040',
                    'fill-outline-color': '#404040',
                    'fill-opacity': 0.1
                }
            },
            {
                'id': 'gl-draw-polygon-stroke-static',
                'type': 'line',
                'filter': ['all', ['==', 'mode', 'static'],
                    ['==', '$type', 'Polygon']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#404040',
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-line-static',
                'type': 'line',
                'filter': ['all', ['==', 'mode', 'static'],
                    ['==', '$type', 'LineString']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': '#404040',
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-point-static',
                'type': 'circle',
                'filter': ['all',
                    ['==', 'mode', 'static'],
                    ['==', '$type', 'Point']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-color': '#404040'
                }
            },

            // end default themes provided by MB Draw
            // end default themes provided by MB Draw
            // end default themes provided by MB Draw
            // end default themes provided by MB Draw




            // new styles for toggling colors
            // new styles for toggling colors
            // new styles for toggling colors
            // new styles for toggling colors

            {
                'id': 'gl-draw-polygon-fill-inactive-color-picker',
                'type': 'fill',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Polygon'],
                    ['!=', 'mode', 'static'],
                    ['has', 'user_portColor']
                ],
                'paint': {
                    'fill-color': ['get', 'user_portColor'],
                    'fill-outline-color': ['get', 'user_portColor'],
                    'fill-opacity': 0.1
                }
            },
            {
                'id': 'gl-draw-polygon-fill-active-color-picker',
                'type': 'fill',
                'filter': ['all', ['==', 'active', 'true'],
                    ['==', '$type', 'Polygon'],
                    ['has', 'user_portColor']
                ],
                'paint': {
                    'fill-color': ['get', 'user_portColor'],
                    'fill-outline-color': ['get', 'user_portColor'],
                    'fill-opacity': 0.1
                }
            },
            {
                'id': 'gl-draw-polygon-midpoint-color-picker',
                'type': 'circle',
                'filter': ['all', ['==', '$type', 'Point'],
                    ['==', 'meta', 'midpoint']
                ],
                'paint': {
                    'circle-radius': 3,
                    'circle-color': '#fbb03b'
                }
            },
            {
                'id': 'gl-draw-polygon-stroke-inactive-color-picker',
                'type': 'line',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Polygon'],
                    ['!=', 'mode', 'static'],
                    ['has', 'user_portColor']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': ['get', 'user_portColor'],
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-polygon-stroke-active-color-picker',
                'type': 'line',
                'filter': ['all', ['==', 'active', 'true'],
                    ['==', '$type', 'Polygon'],
                    ['has', 'user_portColor']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': ['get', 'user_portColor'],
                    'line-dasharray': [0.2, 2],
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-line-inactive-color-picker',
                'type': 'line',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'LineString'],
                    ['!=', 'mode', 'static'],
                    ['has', 'user_portColor']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': ['get', 'user_portColor'],
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-line-active-color-picker',
                'type': 'line',
                'filter': ['all', ['==', '$type', 'LineString'],
                    ['==', 'active', 'true'],
                    ['has', 'user_portColor']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': ['get', 'user_portColor'],
                    'line-dasharray': [0.2, 2],
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-polygon-and-line-vertex-stroke-inactive-color-picker',
                'type': 'circle',
                'filter': ['all', ['==', 'meta', 'vertex'],
                    ['!=', 'active', 'true'],
                    ['==', '$type', 'Point'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-color': '#fff'
                }
            },
            {
                'id': 'gl-draw-polygon-and-line-vertex-inactive-color-picker',
                'type': 'circle',
                'filter': ['all', ['==', 'meta', 'vertex'],
                    ['!=', 'active', 'true'],
                    ['==', '$type', 'Point'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 3,
                    'circle-color': '#fbb03b'
                }
            },
            {
                'id': 'gl-draw-polygon-and-line-vertex-stroke-active-color-picker',
                'type': 'circle',
                'filter': ['all', ['==', 'meta', 'vertex'],
                    ['==', 'active', 'true'],
                    ['==', '$type', 'Point'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 7,
                    'circle-color': '#fff'
                }
            },
            {
                'id': 'gl-draw-polygon-and-line-vertex-active-color-picker',
                'type': 'circle',
                'filter': ['all', ['==', 'meta', 'vertex'],
                    ['==', 'active', 'true'],
                    ['==', '$type', 'Point'],
                    ['!=', 'mode', 'static']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-color': '#fbb03b'
                }
            },
            {
                'id': 'gl-draw-point-point-stroke-inactive-color-picker',
                'type': 'circle',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Point'],
                    ['==', 'meta', 'feature'],
                    ['!=', 'mode', 'static'],
                    ['has', 'user_portColor']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-opacity': 1,
                    'circle-color': '#fff'
                }
            },
            {
                'id': 'gl-draw-point-inactive-color-picker',
                'type': 'circle',
                'filter': ['all', ['==', 'active', 'false'],
                    ['==', '$type', 'Point'],
                    ['==', 'meta', 'feature'],
                    ['!=', 'mode', 'static'],
                    ['has', 'user_portColor']
                ],
                'paint': {
                    'circle-radius': 3,
                    'circle-color': ['get', 'user_portColor']
                }
            },
            {
                'id': 'gl-draw-point-stroke-active-color-picker',
                'type': 'circle',
                'filter': ['all', ['==', '$type', 'Point'],
                    ['==', 'active', 'true'],
                    ['!=', 'meta', 'midpoint'],
                    ['has', 'user_portColor']
                ],
                'paint': {
                    'circle-radius': 7,
                    'circle-color': '#fff'
                }
            },
            {
                'id': 'gl-draw-point-active-color-picker',
                'type': 'circle',
                'filter': ['all', ['==', '$type', 'Point'],
                    ['!=', 'meta', 'midpoint'],
                    ['==', 'active', 'true'],
                    ['has', 'user_portColor']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-color': ['get', 'user_portColor']
                }
            },
            {
                'id': 'gl-draw-polygon-fill-static-color-picker',
                'type': 'fill',
                'filter': ['all', ['==', 'mode', 'static'],
                    ['==', '$type', 'Polygon'],
                    ['has', 'user_portColor']
                ],
                'paint': {
                    'fill-color': ['get', 'user_portColor'],
                    'fill-outline-color': ['get', 'user_portColor'],
                    'fill-opacity': 0.1
                }
            },
            {
                'id': 'gl-draw-polygon-stroke-static-color-picker',
                'type': 'line',
                'filter': ['all', ['==', 'mode', 'static'],
                    ['==', '$type', 'Polygon'],
                    ['has', 'user_portColor']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': ['get', 'user_portColor'],
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-line-static-color-picker',
                'type': 'line',
                'filter': ['all', ['==', 'mode', 'static'],
                    ['==', '$type', 'LineString'],
                    ['has', 'user_portColor']
                ],
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-color': ['get', 'user_portColor'],
                    'line-width': 2
                }
            },
            {
                'id': 'gl-draw-point-static-color-picker',
                'type': 'circle',
                'filter': ['all',
                    ['==', 'mode', 'static'],
                    ['==', '$type', 'Point'],
                    ['has', 'user_portColor']
                ],
                'paint': {
                    'circle-radius': 5,
                    'circle-color': ['get', 'user_portColor']
                }
            }
        ]
    });

    var drawTool = document.getElementById('drawAppend');
    drawTool.appendChild(draw.onAdd(map)).setAttribute("style", "display: inline-flex;", "border: 0;");

    // create draw palette
    function populateDrawPalette() {
        var drawFeatureColor = document.getElementById('customDrawColor');

        for (var c = 0; c < TEXT_COLORS.length; c++) {
            var cElm = document.createElement('div');
            cElm.className = 'draw-color-change';
            cElm.id = 'draw-' + TEXT_COLORS[c];
            cElm.style['background-color'] = TEXT_COLORS[c];
            cElm.addEventListener('mousedown', changeDrawColor);

            drawFeatureColor.appendChild(cElm);
        };
    }

    function handlePolygonOrder(clickedFeats) {
        if (clickedFeats.length > 1) {
            var tempTrack = trackDrawnPolygons.filter(function (p) {
                return clickedFeats.indexOf(p) > -1;
            });

            var lastPoly = tempTrack[tempTrack.length - 1];
            draw.changeMode('direct_select', { featureId: lastPoly });

            var feat = draw.get(lastPoly);
            var c = feat.properties.portColor ? feat.properties.portColor : '#fbb03b';
            handleVerticesColors(c);

        } else if (clickedFeats.length === 1) {

            var feat = draw.get(clickedFeats[0]);
            var c = feat.properties.portColor ? feat.properties.portColor : '#fbb03b';
            handleVerticesColors(c);
        }

        getLastDrawnPoly = false;
    }


    // vertices and midpoints don't inherit their parent properties
    // so we need to handle those edge cases
    function handleVerticesColors(color) {
        // midppoints
        map.setPaintProperty('gl-draw-polygon-midpoint-color-picker.hot', 'circle-color', color);
        map.setPaintProperty('gl-draw-polygon-midpoint-color-picker.cold', 'circle-color', color);

        // vertices
        map.setPaintProperty('gl-draw-polygon-and-line-vertex-inactive-color-picker.cold', 'circle-color', color);
        map.setPaintProperty('gl-draw-polygon-and-line-vertex-inactive-color-picker.hot', 'circle-color', color);

        //active vertex
        map.setPaintProperty('gl-draw-polygon-and-line-vertex-active-color-picker.cold', 'circle-color', color);
        map.setPaintProperty('gl-draw-polygon-and-line-vertex-active-color-picker.hot', 'circle-color', color);
    }

    // color change function of draw features
    var changeDrawColor = function (e) {

        if (e.target.id && e.target.id.indexOf('draw-') === -1) return;

        var color = e.target.id.replace(/draw-/, '');

        if (drawFeatureID !== '' && typeof draw === 'object') {

            draw.setFeatureProperty(drawFeatureID, 'portColor', color);
            var feat = draw.get(drawFeatureID);
            draw.add(feat);

            // race conditions exist between events
            // and draw's transitions between .hot and .cold layers
            setTimeout(function () {
                handleVerticesColors(color);
            }, 50);
        }

    };

    // callback for draw.update and draw.selectionchange
    var setDrawFeature = function (e) {
        if (e.features.length && e.features[0].type === 'Feature') {
            var feat = e.features[0];
            drawFeatureID = feat.id;

            if (feat.geometry.type === 'Polygon' && trackDrawnPolygons.length > 1 && draw.getMode() !== 'draw_polygon' &&
                feat.id !== trackDrawnPolygons[trackDrawnPolygons.length - 1]) {
                getLastDrawnPoly = true;
            } else {
                var c = feat.properties.portColor ? feat.properties.portColor : '#fbb03b';

                // race conditions exist between events
                // and draw's transitions between .hot and .cold layers
                setTimeout(function () {
                    handleVerticesColors(c);
                }, 50);
            }
        }
    };

    // Event Handlers for Draw Tools
    map.on('draw.create', function (e) {
        newDrawFeature = true;
        if (e.features.length && e.features[0].geometry.type === 'Polygon') {
            trackDrawnPolygons.push(e.features[0].id);
        }
    });

    // track handling for polygon features
    map.on('draw.delete', function (e) {
        if (e.features.length) {
            var feats = e.features;
            var featsToRemove = [];

            for (var i = feats.length - 1; i >= 0; i--) {
                featsToRemove.push(feats[i].id);
            }

            var tempTrack = trackDrawnPolygons.filter(function (p) {
                return featsToRemove.indexOf(p) < 0;
            });

            trackDrawnPolygons = tempTrack;
        }
    });

    map.on('draw.update', setDrawFeature);
    map.on('draw.selectionchange', setDrawFeature);

    map.on('click', function (e) {
        if (getLastDrawnPoly) {
            var clickedFeats = draw.getFeatureIdsAt(e.point);
            handlePolygonOrder(clickedFeats);
        } else if (!newDrawFeature) {

            handleVerticesColors('#fbb03b');
            var drawFeatureAtPoint = draw.getFeatureIdsAt(e.point);

            //if another drawFeature is not found - reset drawFeatureID
            drawFeatureID = drawFeatureAtPoint.length ? drawFeatureAtPoint[0] : '';
        }

        newDrawFeature = false;
    });


    //// Turf Area Calc
    var selectedUnits = '';
    var selectedMeasuredFeature = '';
    var measurementActive = false;


    function removeMeasurementValues() {
        $('#calculated-area p').remove();
        $('#calculated-length p').remove();
    }

    function calculateDimensions(data) {
        if (!data.id) return;

        var area, rounded_area, areaAnswer, length, rounded_length, lineAnswer;
        //FEET
        if (selectedUnits === 'feet') {

            area = turf.area(data) / 0.09290304;
            // restrict to 2 decimal points
            rounded_area = Math.round(area * 100) / 100;
            areaAnswer = document.getElementById('calculated-area');
            areaAnswer.innerHTML = '<p>' + rounded_area + ' ft<sup>2</sup></p>';

            length = turf.lineDistance(data, 'meters') / 0.3048;
            // restrict to 2 decimal points
            rounded_length = Math.round(length * 100) / 100;
            lineAnswer = document.getElementById('calculated-length');
            lineAnswer.innerHTML = '<p>' + rounded_length + ' ft</p>';

            //METER
        } else if (selectedUnits === 'meter') {

            area = turf.area(data);
            // restrict to 2 decimal points
            rounded_area = Math.round(area * 100) / 100;
            areaAnswer = document.getElementById('calculated-area');
            areaAnswer.innerHTML = '<p>' + rounded_area + ' m<sup>2</sup></p>';

            length = turf.lineDistance(data, 'meters');
            // restrict to 2 decimal points
            rounded_length = Math.round(length * 100) / 100;
            lineAnswer = document.getElementById('calculated-length');
            lineAnswer.innerHTML = '<p>' + rounded_length + ' m</p>';

            //MILE
        } else if (selectedUnits === 'mile') {

            area = turf.area(data) / 2589988.11;
            // restrict to 4 decimal points
            rounded_area = Math.round(area * 10000) / 10000;
            areaAnswer = document.getElementById('calculated-area');
            areaAnswer.innerHTML = '<p>' + rounded_area + ' mi<sup>2</sup></p>';

            length = turf.lineDistance(data, 'meters') / 1609.344;
            // restrict  to 2 decimal points
            rounded_length = Math.round(length * 100) / 100;
            lineAnswer = document.getElementById('calculated-length');
            lineAnswer.innerHTML = '<p>' + rounded_length + ' mi</p>';

            //KILOMETER
        } else if (selectedUnits === 'kilometer') {

            area = turf.area(data) / 1000000;
            // restrict to 4 decimal points
            rounded_area = Math.round(area * 10000) / 10000;
            areaAnswer = document.getElementById('calculated-area');
            areaAnswer.innerHTML = '<p>' + rounded_area + ' km<sup>2</sup></p>';

            length = turf.lineDistance(data, 'meters') / 1000;
            // restrict to 2 decimal points
            rounded_length = Math.round(length * 100) / 100;
            lineAnswer = document.getElementById('calculated-length');
            lineAnswer.innerHTML = '<p>' + rounded_length + ' km</p>';

            //ACRE
        } else if (selectedUnits === 'acre') {

            area = turf.area(data) / 4046.85642;
            // restrict  to 4 decimal points
            rounded_area = Math.round(area * 10000) / 10000;
            areaAnswer = document.getElementById('calculated-area');
            areaAnswer.innerHTML = '<p>' + rounded_area + ' acres</p>';

            length = turf.lineDistance(data, 'meters') / 0.3048;
            // restrict to 2 decimal points
            rounded_length = Math.round(length * 100) / 100;
            lineAnswer = document.getElementById('calculated-length');
            lineAnswer.innerHTML = '<p>' + rounded_length + ' ft</p>';

        }
    }

    // callback fires on the events listed below and fires the
    // above calculateDimensions function
    var calculateCallback = function (e) {
        if (e.features.length && (e.features[0].geometry.type === 'Polygon' || e.features[0].geometry.type === 'LineString')) {
            measurementActive = true;
            selectedMeasuredFeature = e.features[0].id;
            calculateDimensions(e.features[0]);
        }
    }

    map.on('draw.create', calculateCallback);
    map.on('draw.update', calculateCallback);
    map.on('draw.selectionchange', calculateCallback);

    map.on('draw.delete', function (e) {
        selectedMeasuredFeature = '';
        measurementActive = false;
        removeMeasurementValues();
    });

    // apparently there's no method to track/watch a drag or vertex
    // of a newly instantiated feature that has yet to be 'created'
    // or perhaps it's not documented anywhere in GL Draw
    // so we have to make our own
    map.on('mousemove', function (e) {
        if (draw.getMode() === 'draw_line_string' || draw.getMode() === 'draw_polygon') {
            var linePts = draw.getFeatureIdsAt(e.point);

            if (linePts.length) {
                // some draw features return back as undefined
                var activeID = linePts.filter(function (feat) {
                    return typeof feat === 'string';
                })

                if (activeID.length) {
                    measurementActive = true;
                    selectedMeasuredFeature = activeID[0];

                    var fc = draw.get(selectedMeasuredFeature);
                    calculateDimensions(fc);
                }
            }
        } else if (draw.getMode() === 'direct_select' && selectedMeasuredFeature !== '') {
            var fc = draw.get(selectedMeasuredFeature);

            if (fc.geometry.type === 'LineString' || fc.geometry.type === 'Polygon') {
                calculateDimensions(fc);
            }

        }
    });

    // remove measurements from input
    map.on('click', function (e) {
        if (measurementActive) {
            var measuredFeature = draw.getFeatureIdsAt(e.point);

            if (measuredFeature.length) {
                // some draw features return back as undefined
                var mF = measuredFeature.filter(function (feat) {
                    return typeof feat === 'string';
                })

                selectedMeasuredFeature = mF.length ? mF[0] : '';

            } else {
                removeMeasurementValues();
            }
        } else {
            removeMeasurementValues();
        }

        measurementActive = false;
    });


    $(function () {
        // set unit value
        selectedUnits = $('input[type=radio][name=unit]:checked').val();

        $('input[type=radio][name=unit]').change(function () {
            selectedUnits = this.value;

            //update values based on new units
            if (selectedMeasuredFeature !== '' || measurementActive) {
                var gj = draw.get(selectedMeasuredFeature);
                calculateDimensions(gj);
            }
        })

        populateDrawPalette();
    });


    // $$\      $$\                             $$\                $$$$$$\   $$$$$$\  
    // $$$\    $$$ |                            $$ |              $$  __$$\ $$  __$$\ 
    // $$$$\  $$$$ |$$\   $$\        $$$$$$$\ $$$$$$\   $$\   $$\ $$ /  \__|$$ /  \__|
    // $$\$$\$$ $$ |$$ |  $$ |      $$  _____|\_$$  _|  $$ |  $$ |$$$$\     $$$$\     
    // $$ \$$$  $$ |$$ |  $$ |      \$$$$$$\    $$ |    $$ |  $$ |$$  _|    $$  _|    
    // $$ |\$  /$$ |$$ |  $$ |       \____$$\   $$ |$$\ $$ |  $$ |$$ |      $$ |      
    // $$ | \_/ $$ |\$$$$$$$ |      $$$$$$$  |  \$$$$  |\$$$$$$  |$$ |      $$ |      
    // \__|     \__| \____$$ |      \_______/    \____/  \______/ \__|      \__|      
    //              $$\   $$ |                                                        
    //              \$$$$$$  |                                                        
    //               \______/                                                         
    // My Stuff
    map.on(touchEvent, function (e) {
        var radio = document.getElementById('point1');

        if (radio.checked == true) {
            point = 'info1';
        }
        else
            point = 'info2';

        document.getElementById(point).innerHTML =
            JSON.stringify(e.lngLat, function (key, val) { return val.toFixed ? Number(val.toFixed(4)) : val; }).replace('{"lng":', '').replace('"lat":', ' ').replace('}', '')
        console.log(JSON.stringify(e.lngLat, function (key, val) { return val.toFixed ? Number(val.toFixed(4)) : val; }).replace('{"lng":', '').replace('"lat":', ' ').replace('}', ''))
        e.preventDefault();
    });



    map.on('mousemove', function (e) {
        if (draw.getMode() === 'draw_line_string' || draw.getMode() === 'draw_polygon') {
            var linePts = draw.getFeatureIdsAt(e.point);

            if (linePts.length) {
                // some draw features return back as undefined
                var activeID = linePts.filter(function (feat) {
                    return typeof feat === 'string';
                })

                if (activeID.length) {
                    measurementActive = true;
                    selectedMeasuredFeature = activeID[0];

                    var fc = draw.get(selectedMeasuredFeature);
                    calculateDimensions(fc);
                }
            }
        } else if (draw.getMode() === 'direct_select' && selectedMeasuredFeature !== '') {
            var fc = draw.get(selectedMeasuredFeature);

            if (fc.geometry.type === 'LineString' || fc.geometry.type === 'Polygon') {
                calculateDimensions(fc);
            }

        }
    });