"""GIS utilities"""
from __future__ import division
import math


def meters_to_degrees(distance_in_meters, radius):
    try:
        float(distance_in_meters)
        float(radius)
        if distance_in_meters < 0:
            raise ValueError("distance_in_meters must be a positive number")
        if radius <= 0:
            raise ValueError("radius must be a positive number and larger than zero")
    except ValueError:
        raise

    return math.degrees(distance_in_meters / radius)