from django.test import SimpleTestCase
from django.contrib.gis.geos import Point

from ..utils import grid_to_point, point_to_grid, address_to_point, address_to_grid_based_point


class LocationTestCase(SimpleTestCase):
    def setUp(self):
        self.grids = (
            ("JN58ki", Point(10.873333, 48.353333)),
            ("FK18fi", Point(-77.543333, 18.353333)),
            ("RH82xe", Point(177.956667, -17.813333)),
        )

        self.address = (
            ("Augsburg, Germany", Point(10.897910, 48.368932)),
            ("69 Westminister Rd, Kingston, Jamaika", Point(-76.800375, 18.020925)),
            ("Rahmon Nabiyev Street, Dushanbe, Tadschikistan", Point(68.746526, 38.542975)),
        )

    def test_grid_to_point(self):
        for grid, point in self.grids:
            with self.subTest(i=grid):
                grid_point = grid_to_point(grid)
                self.assertLess(grid_point.distance(point), 0.1)

    def test_point_to_grid(self):
        for grid, point in self.grids:
            with self.subTest(i=grid):
                self.assertEqual(point_to_grid(point), grid)

    def test_address_to_point(self):
        for address, point in self.address:
            with self.subTest(i=address):
                self.assertLess(address_to_point(address, use_cache=False).distance(point), 0.1)

    def test_address_to_grid_based_point(self):
        for address, point in self.address:
            with self.subTest(i=address):
                self.assertLess(address_to_grid_based_point(address, use_cache=False).distance(point), 0.1)
