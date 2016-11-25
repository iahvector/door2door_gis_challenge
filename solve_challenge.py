import sys
import getopt
import os.path
import json


def main(argv):
    points_file = None
    routes_file = None

    options_list = ["points=", "routes="]
    help_msg = "solve_challenge.py --points=</path/to/points.geojson> --routes=</path/to/routes.geojson>"

    if len(argv) != 2:
        print help_msg
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "", options_list)
    except getopt.GetoptError:
        print help_msg
        sys.exit(2)

    try:
        for opt, arg in opts:
            if opt == "--points":
                if os.path.isfile(arg):
                    points_file = arg
                else:
                    raise IOError(filename=arg)
            elif opt == "--routes":
                if os.path.isfile(arg):
                    routes_file = arg
                else:
                    raise IOError(filename=arg)
    except IOError as e:
        print e.filename + " is not a vaild file"
        sys.exit(2)

    points = None
    routes = None
    with open(points_file, 'r') as pf, open(routes_file, 'r') as rf:
        points = json.load(pf)
        routes = json.load(rf)

    # Solve challenge

if __name__ == "__main__":
    main(sys.argv[1:])