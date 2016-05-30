import unittest
from gurpsspace import planetsystem, star


class TestPlanetsystem(unittest.TestCase):

    def setUp(self):
        self.mystar = star.Star(age=4)
        self.myplansys = planetsystem.PlanetSystem(self.mystar)
