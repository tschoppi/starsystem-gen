import unittest
from gurpsspace import starsystem


class TestStarsystem(unittest.TestCase):

    def setUp(self):
        self.system = starsystem.StarSystem()

    def test_generate_starsystem_open_cluster_one_star(self):
        arguments = {
            'open_cluster': "True",
            'num_stars': 1,
            'age': None
        }
        self.testsystem = starsystem.StarSystem(**arguments)

    def test_age_check(self):
        self.assertRaises(ValueError, self.system.make_age, age=0)
        self.assertRaises(ValueError, self.system.make_age, age=-2.4)

    def test_age_generation(self):
        self.assertTrue(self.system.make_age() > 0)

    def test_random_age(self):
        self.assertTrue(self.system.random_age() > 0)

    def test_find_orbital_separation_index(self):
        self.assertRaises(ValueError, self.system.find_orbital_separation_index, dice_roll=2)
        self.assertRaises(ValueError, self.system.find_orbital_separation_index, dice_roll=-2)

    def test_descending_sort(self):
        arguments = {'num_stars': 2}
        testsystem = starsystem.StarSystem(**arguments)
        self.assertTrue(testsystem.stars[0].get_mass() >= testsystem.stars[1].get_mass())

    def test_orbit_generation(self):
        unisystem = starsystem.StarSystem(num_stars=1)
        bisystem = starsystem.StarSystem(num_stars=2)
        trisystem = starsystem.StarSystem(num_stars=3)
        self.assertTrue(len(unisystem.orbits) == 0)
        self.assertTrue(len(bisystem.orbits) == 1)
        self.assertTrue(len(trisystem.orbits) == 2)
        self.assertTrue(trisystem.orbits[1][0] > trisystem.orbits[0][0])
