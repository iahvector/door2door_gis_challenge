import sys
import getopt
import os.path
import json
import pprint
import door2door.challenges.gis.solution


def main(argv):
    points_file = None
    routes_file = None

    options_list = ["points=", "routes="]
    help_msg = "solve_challenge.py --points=</path/to/points.geojson> --routes=</path/to/routes.geojson>"

    if len(argv) != 2:
        print(help_msg)
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "", options_list)
    except getopt.GetoptError:
        print(help_msg)
        sys.exit(2)

    try:
        for opt, arg in opts:
            if opt == "--points":
                if os.path.isfile(arg):
                    points_file = arg
                else:
                    raise Exception(arg)
            elif opt == "--routes":
                if os.path.isfile(arg):
                    routes_file = arg
                else:
                    raise Exception(arg)
    except Exception as e:
        print(str(e.args[0]) + " is not a valid file")
        sys.exit(2)

    points = None
    routes = None
    with open(points_file, "r") as pf, open(routes_file, "r") as rf:
        points = json.load(pf)
        routes = json.load(rf)

    points_formatted = []
    for f in points["features"]:
        points_formatted.append({
            "coordinates": {
                "lat": f["geometry"]["coordinates"][1],
                "lng": f["geometry"]["coordinates"][0]
            },
            "meta": f["properties"]
        })

    routes_formatted = {
        "MultiLineString": []
    }
    for f in routes["features"]:
        routes_formatted["MultiLineString"].append(f["geometry"]["coordinates"])

    # TODO Validate data to be GeoJSON with proper properties schema for feature object

    result = door2door.challenges.gis.solution.solve(points=points_formatted,
                                                     activity_bias=[
                                                         {
                                                             "previous_dominating_activity": "none",
                                                             "current_dominating_activity": "none",
                                                             "weight": 1
                                                         },
                                                         {
                                                             "previous_dominating_activity": "none",
                                                             "current_dominating_activity": "still",
                                                             "weight": 100
                                                         },
                                                         {
                                                             "previous_dominating_activity": "none",
                                                             "current_dominating_activity": "on_foot",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "none",
                                                             "current_dominating_activity": "on_bicycle",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "none",
                                                             "current_dominating_activity": "in_vehicle",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "still",
                                                             "current_dominating_activity": "none",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "still",
                                                             "current_dominating_activity": "still",
                                                             "weight": 1000
                                                         },
                                                         {
                                                             "previous_dominating_activity": "still",
                                                             "current_dominating_activity": "on_foot",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "still",
                                                             "current_dominating_activity": "on_bicycle",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "still",
                                                             "current_dominating_activity": "in_vehicle",
                                                             "weight": 1000
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_foot",
                                                             "current_dominating_activity": "none",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_foot",
                                                             "current_dominating_activity": "still",
                                                             "weight": 1000
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_foot",
                                                             "current_dominating_activity": "on_foot",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_foot",
                                                             "current_dominating_activity": "on_bicycle",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_foot",
                                                             "current_dominating_activity": "in_vehicle",
                                                             "weight": 1000
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_bicycle",
                                                             "current_dominating_activity": "none",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_bicycle",
                                                             "current_dominating_activity": "still",
                                                             "weight": 1000
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_bicycle",
                                                             "current_dominating_activity": "on_foot",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_bicycle",
                                                             "current_dominating_activity": "on_bicycle",
                                                             "weight": 10
                                                         },
                                                         {
                                                             "previous_dominating_activity": "on_bicycle",
                                                             "current_dominating_activity": "in_vehicle",
                                                             "weight": 1000
                                                         },
                                                         {
                                                             "previous_dominating_activity": "in_vehicle",
                                                             "current_dominating_activity": "none",
                                                             "weight": 100
                                                         },
                                                         {
                                                             "previous_dominating_activity": "in_vehicle",
                                                             "current_dominating_activity": "still",
                                                             "weight": 1000
                                                         },
                                                         {
                                                             "previous_dominating_activity": "in_vehicle",
                                                             "current_dominating_activity": "on_foot",
                                                             "weight": 1000
                                                         },
                                                         {
                                                             "previous_dominating_activity": "in_vehicle",
                                                             "current_dominating_activity": "on_bicycle",
                                                             "weight": 1000
                                                         },
                                                         {
                                                             "previous_dominating_activity": "in_vehicle",
                                                             "current_dominating_activity": "in_vehicle",
                                                             "weight": 10
                                                         }
                                                     ],
                                                     routes=routes_formatted,
                                                     margin_meters=150,
                                                     mean_earth_radius=6371000)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(result)


if __name__ == "__main__":
    main(sys.argv[1:])
