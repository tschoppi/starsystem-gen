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
