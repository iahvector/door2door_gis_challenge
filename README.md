# door2door_gis_challenge
An attempt to solve Door2Door GIS developer challenge https://github.com/door2door-io/gis-code-challenge

## Setup:

1- Install [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

2- Install [shapely requirements](http://toblerity.org/shapely/project.html#requirements)

On ubuntu 16.04 
```bash
$ sudo apt install libgeos-*
```

3- Clone this repository and change directory to `door2door_gis_challenge`

4- Create a new virtualenv and activate it
```bash
$ virtualenv -p /usr/bin/python2.7 venv
$ source venv/bin/activate
```

5- Install requirements
```bash
$ pip install -r requirements.txt
```

## Usage
1- Run the script
```bash
$ python solve_challenge.py --points=data/activity_points.geojson --routes=data/routes.geojson > data/out.geojson
```

2- Open index.html in a web browser
  * Bus routes are rendered in blue
  * Croud sourced data are rendered as small orange circles
  * Solution output is is rendered as blue markers
  
## TODO
* Enhance clustering
* Wrap in flask
  - Upload activity and routes files and adjust algorithm parameters via REST API
  - Make the web page use the REST API to send the files and parameters and load the result dynamically
* Create docker image for easier installation of the solution

