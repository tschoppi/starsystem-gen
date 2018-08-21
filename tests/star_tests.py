import unittest
from gurpsspace import star


class TestStar(unittest.TestCase):

    def setUp(self):
        self.mystar = star.Star(age=2.5)

    def test_init(self):
        self.assertRaises(ValueError, star.Star, age=-1.0)
        self.assertRaises(ValueError, star.Star, age=0)

    def test_set_forbidden_zone(self):
        self.assertRaises(ValueError, self.mystar.set_forbidden_zone, inner=2, outer=1)
        self.assertRaises(ValueError, self.mystar.set_forbidden_zone, 2, 2)

    def test_orbit_limits(self):
        orblim = self.mystar.get_orbit_limits()
        self.assertTrue(orblim[0] < orblim[1])

    def test_snowline(self):
        self.assertTrue(self.mystar.get_snowline() > 0)

    def test_luminosity(self):
        self.assertTrue(self.mystar.get_luminosity() > 0)

    def test_forbidden_zone(self):
        self.assertFalse(self.mystar.has_forbidden_zone())
        self.mystar.set_forbidden_zone(1, 2)
        self.assertTrue(self.mystar.has_forbidden_zone())
        forbzone = self.mystar.get_forbidden_zone()
        self.assertEqual(forbzone[0], 1)
        self.assertEqual(forbzone[1], 2)

    def test_radius(self):
        self.assertTrue(self.mystar.get_radius() > 0)

    def test_letter(self):
        self.assertEqual(self.mystar.get_letter(), 'A')

        self.mystar.set_letter('B')
        self.assertEqual(self.mystar.get_letter(), 'B')

    def test_get_spectral_type(self):
        sp_index = min(range(len(StEvoTable['temp'])),
                       key=lambda i: abs(StEvoTable['temp'][i] - self.get_temperature()))
        self.assertTrue(StEvoTable['type'][sp_index])
