/**
 * Created by islamhassan on 11/20/16.
 */


// Separate access token for GIS code Challenge. Insecure but included here for simplicity
var MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiaWFodmVjdG9yIiwiYSI6ImNpdnF3bDR5bTAwMXYydHBqMmd1Z3ZqamgifQ.Z2ErUL5ZNyTV3qOUtuccHg';
var MAPBOX_MAP_ID = 'streets-v10';
var MAPBOX_TILES_URL_TEMPLATE = 'https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{tileQuality}/{z}/{x}/{y}?access_token={accessToken}';
var MAPBOX_ATTRIBUTION = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,' +
  ' <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>';
var MAPBOX_MAX_ZOOM_LEVEL = 18;
var MAPBOX_TILE_QUALITY = 256;

var DAR_EL_SALAM_COORDS = [-6.8, 39.283333];
var INITIAL_ZOOM_LEVEL = 13;

var map = L.map('gismap').setView(DAR_EL_SALAM_COORDS, INITIAL_ZOOM_LEVEL);
L.tileLayer(MAPBOX_TILES_URL_TEMPLATE, {
  attribution: MAPBOX_ATTRIBUTION,
  maxZoom: MAPBOX_MAX_ZOOM_LEVEL,
  tileQuality: MAPBOX_TILE_QUALITY,
  id: MAPBOX_MAP_ID,
  accessToken: MAPBOX_ACCESS_TOKEN
}).addTo(map);

$('#gismap').height($(window).height()).width($(window).width());
map.invalidateSize();

$.getJSON('data/routes.geojson', function (response) {
  L.geoJSON(response).addTo(map);
});

var geojsonMarkerOptions = {
    radius: 5,
    fillColor: "#ff7800",
    color: "#000",
    weight: 1,
    opacity: 1,
    fillOpacity: 0.8
};

$.getJSON('data/activity_points.geojson', function (response) {
  L.geoJSON(response, {
    pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, geojsonMarkerOptions);
    }
  }).addTo(map);
});

try {
  $.getJSON('data/out.geojson', function (response) {
    L.geoJSON(response).addTo(map);
  });
} catch (e) {
  // Pass
}
