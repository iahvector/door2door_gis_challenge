"""Test the door2door.challenges.gis.solution module"""

import unittest2
from door2door.challenges.gis import solution


class SolutionTest(unittest2.TestCase):
    def test_assign_activity_weights(self):
        weights = [
            {
                "previous_dominating_activity": "none",
                "current_dominating_activity": "none",
                "weight": 1
            },
            {
                "previous_dominating_activity": "none",
                "current_dominating_activity": "on_foot",
                "weight": 10
            },
            {
                "previous_dominating_activity": "none",
                "current_dominating_activity": "still",
                "weight": 100
            },
            {
                "previous_dominating_activity": "still",
                "current_dominating_activity": "still",
                "weight": 1000
            }
        ]

        points = [
            {
                "coordinates": {
                    "lat": 42,
                    "lng": 42
                },
                "meta": {
                    "previous_dominating_activity": "none",
                    "current_dominating_activity": "none",
                    "previous_dominating_activity_confidence": 0,
                    "current_dominating_activity_confidence": 0,
                    "accuracy": 10.0
                }
            },
            {
                "coordinates": {
                    "lat": 42,
                    "lng": 42
                },
                "meta": {
                    "previous_dominating_activity": "none",
                    "current_dominating_activity": "on_foot",
                    "previous_dominating_activity_confidence": 0,
                    "current_dominating_activity_confidence": 50,
                    "accuracy": 50.0
                }
            },
            {
                "coordinates": {
                    "lat": 42,
                    "lng": 42
                },
                "meta": {
                    "previous_dominating_activity": "none",
                    "current_dominating_activity": "still",
                    "previous_dominating_activity_confidence": 0,
                    "current_dominating_activity_confidence": 70,
                    "accuracy": 130.0
                }
            },
            {
                "coordinates": {
                    "lat": 42,
                    "lng": 42
                },
                "meta": {
                    "previous_dominating_activity": "still",
                    "current_dominating_activity": "still",
                    "previous_dominating_activity_confidence": 20,
                    "current_dominating_activity_confidence": 60,
                    "accuracy": 100.0
                }
            }
        ]

        with self.subTest(msg="Test: Assigns weights correctly"):
            weighted_points = solution.assign_activity_weights(points, weights)
            self.assertEqual(len(weighted_points), 4)
            self.assertAlmostEqual(weighted_points[0]["meta"]["weight"], 0.1, 2)
            self.assertAlmostEqual(weighted_points[1]["meta"]["weight"], 10.0, 2)
            self.assertAlmostEqual(weighted_points[2]["meta"]["weight"], 53.8461538462, 2)
            self.assertAlmostEqual(weighted_points[3]["meta"]["weight"], 12000.0, 2)

    def test_filter_points_by_routes(self):
        points = [
            {
                "coordinates": {
                    "lat": 0.005,
                    "lng": 0.005
                },
            },
            {
                "coordinates": {
                    "lat": -0.005,
                    "lng": 0.005
                },
            },
            {
                "coordinates": {
                    "lat": 0.005,
                    "lng": 0
                },
            }
        ]
        routes = {
            "MultiLineString": [
                [[0, 0], [0, 0.01]]
            ]
        }
        margin_meters = 150
        mean_earth_radius = 6371000

        with self.subTest(msg="Test: Filters points correctly"):
            filtered_points = solution.filter_points_by_routes(points, routes, margin_meters, mean_earth_radius)
            self.assertEqual(len(filtered_points), 1)
            self.assertEqual(filtered_points, [{"coordinates": {"lat": 0.005, "lng": 0}, }])

    def test_cluster_points_by_distance(self):
        points = [
            {
                "coordinates": {
                    "lng": 0,
                    "lat": 0
                }
            },
            {
                "coordinates": {
                    "lng": 0,
                    "lat": 0.0001
                }
            },
            {
                "coordinates": {
                    "lng": 0,
                    "lat": 0.0002
                }
            },
            {
                "coordinates": {
                    "lng": 0,
                    "lat": 0.0003
                }
            },
            {
                "coordinates": {
                    "lng": 0,
                    "lat": 0.001
                }
            },
            {
                "coordinates": {
                    "lng": 0,
                    "lat": 0.0011
                }
            },
            {
                "coordinates": {
                    "lng": 0,
                    "lat": 0.0012
                }
            },
            {
                "coordinates": {
                    "lng": 0,
                    "lat": 0.0013
                }
            }
        ]

        with self.subTest(msg="Test: Clusters points correctly"):
            clusters = solution.cluster_points_by_distance(points, 100, 6371000)
            self.assertEqual(len(clusters), 2)
            self.assertEqual(len(clusters[0]), 4)
            self.assertEqual(len(clusters[1]), 4)
            self.assertEqual(clusters, [
                [
                    {
                        "coordinates": {
                            "lng": 0,
                            "lat": 0
                        }
                    },
                    {
                        "coordinates": {
                            "lng": 0,
                            "lat": 0.0001
                        }
                    },
                    {
                        "coordinates": {
                            "lng": 0,
                            "lat": 0.0002
                        }
                    },
                    {
                        "coordinates": {
                            "lng": 0,
                            "lat": 0.0003
                        }
                    }
                ],
                [
                    {
                        "coordinates": {
                            "lng": 0,
                            "lat": 0.001
                        }
                    },
                    {
                        "coordinates": {
                            "lng": 0,
                            "lat": 0.0011
                        }
                    },
                    {
                        "coordinates": {
                            "lng": 0,
                            "lat": 0.0012
                        }
                    },
                    {
                        "coordinates": {
                            "lng": 0,
                            "lat": 0.0013
                        }
                    }
                ]
            ])
