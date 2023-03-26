import unittest

import pygame

from ship import Ship

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

    def test_ship_move(self):
        ship = Ship(vector2(50, 60))
        ship.velocity = vector2(10, 16)
        ship.move(0.5)
        self.assertEqual(ship.position, vector2(55, 68))

    def test_ship_acceleration(self):
        ship = Ship(vector2(0, 0))
        ship.angle = 45
        ship.acceleration = 100
        ship.power_on(1.0)
        self.assertAlmostEqual(ship.velocity.x, 70.7106, 2, "x value")
        self.assertAlmostEqual(ship.velocity.y, -70.7106, 2, "y value")



if __name__ == '__main__':
    unittest.main()
