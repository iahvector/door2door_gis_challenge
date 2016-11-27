"""Unit tests for module door2door.utils.gis"""
import unittest2
from door2door.utils import gis
import math


class GisUtilsTest(unittest2.TestCase):
    def test_meters_to_degrees(self):
        radius = 10
        half_circumference = radius * math.pi
        with self.subTest(msg="Test: Converts distance from meters to degrees correctly"):
            deg = gis.meters_to_degrees(half_circumference, radius)
            self.assertEqual(deg, 180)

        with self.subTest(msg="Test: Raises ValueError when a a wrong value or type is passed"):
            with self.assertRaises(ValueError):
                gis.meters_to_degrees(-1, radius)
            with self.assertRaises(ValueError):
                gis.meters_to_degrees(half_circumference, 0)
            with self.assertRaises(ValueError):
                gis.meters_to_degrees(half_circumference, -1)
            with self.assertRaises(ValueError):
                gis.meters_to_degrees(-1, -1)
            with self.assertRaises(ValueError):
                gis.meters_to_degrees(half_circumference, 'string')
            with self.assertRaises(ValueError):
                gis.meters_to_degrees('string', radius)