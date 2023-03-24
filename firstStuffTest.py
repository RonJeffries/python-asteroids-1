import unittest

import pygame

vector2 = pygame.Vector2


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    def test_map_lambda(self):
        points = [vector2(-3.0, -2.0), vector2(-3.0, 2.0), vector2(-5.0, 4.0),
                  vector2(7.0, 0.0), vector2(-5.0, -4.0), vector2(-3.0, -2.0)]
        new_points = map(lambda point: point + vector2(7,4), points)
        for point in new_points:
            self.assertGreaterEqual(point.x, 0)
            self.assertLessEqual(point.x, 14)
            self.assertGreaterEqual(point.y, 0)
            self.assertLessEqual(point.y, 9)


if __name__ == '__main__':
    unittest.main()
