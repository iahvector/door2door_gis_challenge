"""A solution for the Door2Door GIS challenge: https://github.com/door2door-io/gis-code-challenge"""
from __future__ import division
from shapely.geometry import Point, MultiPoint, MultiLineString
from door2door.utils import gis


def solve(points, activity_bias, routes, margin_meters, mean_earth_radius, cluster_radius):
    """Solve the GIS challenge"""
    weighted_points = assign_activity_weights(points, activity_bias)
    filtered_points = filter_points_by_routes(weighted_points, routes, margin_meters, mean_earth_radius)
    clusters = cluster_points_by_distance(filtered_points, cluster_radius, mean_earth_radius)
    centroids = reduce_clusters_to_centroids(clusters)
    return centroids


def assign_activity_weights(points, activity_bias):
    """Assign a certain weight to each point according to activity bias, confidence and measurement accuracy"""
    bias_by_pda_cda = {}
    # Use (pda, cda) tuples as dict keys for easy access
    for b in activity_bias:
        bias_by_pda_cda[(b["previous_dominating_activity"], b["current_dominating_activity"])] = b["weight"]

    for i in range(0, len(points)):
        pda = points[i]["meta"]["previous_dominating_activity"] \
            if points[i]["meta"]["previous_dominating_activity"] is not None \
            else 'none'
        cda = points[i]["meta"]["current_dominating_activity"] \
            if points[i]["meta"]["current_dominating_activity"] is not None \
            else 'none'

        pda_confidence = points[i]["meta"]["previous_dominating_activity_confidence"]
        cda_confidence = points[i]["meta"]["current_dominating_activity_confidence"]
        accuracy = points[i]["meta"]["accuracy"]
        bias = bias_by_pda_cda[(pda, cda)]

        points[i]["meta"]["weight"] = weight_function(bias, pda_confidence, cda_confidence, accuracy)

    return points


def weight_function(bias, previous_activity_confidence, current_activity_confidence, accuracy):
    """Calculate the weight to be assigned to each point based on activity bias, confidence and measurement accuracy"""
    # Make sure no value is 0 to avoid multiplication or division by 0
    bias = bias if bias > 0 else 1
    previous_activity_confidence = previous_activity_confidence if previous_activity_confidence > 0 else 1
    current_activity_confidence = current_activity_confidence if current_activity_confidence > 0 else 1
    accuracy = accuracy if accuracy > 0 else 1
    # Weigh is directly proportional to  bias, previous activity confidence and current activity confidence and is
    # inversely proportional to accuracy (assuming accuracy is in meters, accuracy decreases as the value increases,
    # e.g. accuracy of 10 means that the measurement is accurate up to 10 meters, while an accuracy of 100 means that
    # the measurement is accurate up to 100 meters)
    return (bias * previous_activity_confidence * current_activity_confidence) / accuracy


def filter_points_by_routes(points, routes, margin_meters, mean_earth_radius):
    """Filter points that are on routes with tolerance of margin_meters"""
    routes_shape = MultiLineString(routes["MultiLineString"])
    routes_buffered = routes_shape.buffer(gis.meters_to_degrees(margin_meters, mean_earth_radius))
    filtered = []
    for point in points:
        if routes_buffered.contains(Point(point["coordinates"]["lng"], point["coordinates"]["lat"])):
            filtered.append(point)
    return filtered


def cluster_points_by_distance(points, distance_meters, radius):
    """Group all points within distance_meters from each others into clusters"""
    distance_degrees = gis.meters_to_degrees(distance_meters, radius)
    clusters = []

    while points:
        p1 = Point(points[0]["coordinates"]["lng"], points[0]["coordinates"]["lat"])
        cluster = [points.pop(0)]

        index = 0
        while index < len(points):
            p2 = Point(Point(points[index]["coordinates"]["lng"], points[index]["coordinates"]["lat"]))
            d = p1.distance(p2)
            if d < distance_degrees:
                # If a point is popped, the next point will be shifted to the same index, so do not increment index
                cluster.append(points.pop(index))
            else:
                index += 1

        clusters.append(cluster)

    return clusters


def reduce_clusters_to_centroids(clusters):
    """Reduce clusters into centroids representing the geometric center of each cluster"""
    centroids = []

    for c in clusters:
        points = []
        average_weight = 0
        for p in c:
            points.append((p["coordinates"]["lng"], p["coordinates"]["lat"]))
            average_weight += p["meta"]["weight"]
        average_weight /= len(c)

        cluster_shape = MultiPoint(points)
        centroid = cluster_shape.centroid
        centroids.append({
            "coordinates": {
                "lat": centroid.y,
                "lng": centroid.x
            },
            "meta": {
                "weight": average_weight
            }
        })

    return centroids
