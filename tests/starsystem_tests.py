import unittest
from gurpsspace import starsystem

class TestStarsystem(unittest.TestCase):

    def test_generate_starsystem_open_cluster_one_star(self):
        arguments = {
            'open_cluster': "True",
            'num_stars': 1,
            'age': None
        }
        self.system = starsystem.StarSystem(**arguments)
