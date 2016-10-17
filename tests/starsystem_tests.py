import unittest
from gurpsspace import starsystem


class TestStarsystem(unittest.TestCase):

    def setUp(self):
        self.unisystem = starsystem.StarSystem(num_stars=1)
        self.bisystem = starsystem.StarSystem(num_stars=2)
        self.trisystem = starsystem.StarSystem(num_stars=3)
        self.randomsystem = starsystem.StarSystem()

    def test_generate_starsystem_open_cluster_one_star(self):
        arguments = {
            'open_cluster': "True",
            'num_stars': 1,
            'age': None
        }
        self.testsystem = starsystem.StarSystem(**arguments)

    def test_make_open_cluster_kwarg(self):
        self.assertTrue(self.randomsystem.make_open_cluster(True))
        self.assertFalse(self.randomsystem.make_open_cluster(False))

    def test_make_number_of_stars_kwarg(self):
        self.assertTrue(self.randomsystem.make_number_of_stars(1) == 1)
        self.assertTrue(self.randomsystem.make_number_of_stars(2) == 2)
        self.assertTrue(self.randomsystem.make_number_of_stars(3) == 3)
        self.assertTrue(self.randomsystem.make_number_of_stars(4) != 4)

    def test_age_check(self):
        self.assertRaises(ValueError, self.randomsystem.make_age, age=0)
        self.assertRaises(ValueError, self.randomsystem.make_age, age=-2.4)

    def test_age_generation(self):
        self.assertTrue(self.randomsystem.make_age() > 0)

    def test_random_age(self):
        self.assertTrue(self.randomsystem.random_age() > 0)

    def test_find_orbital_separation_index(self):
        self.assertRaises(
            ValueError,
            self.randomsystem.find_orbital_separation_index,
            dice_roll=2
        )
        self.assertRaises(
            ValueError,
            self.randomsystem.find_orbital_separation_index,
            dice_roll=-2
        )

    def test_descending_sort(self):
        arguments = {'num_stars': 2}
        testsystem = starsystem.StarSystem(**arguments)
        self.assertTrue(
            testsystem.stars[0].get_mass() >= testsystem.stars[1].get_mass()
        )

    def test_orbit_generation(self):
        self.assertTrue(len(self.unisystem.orbits) == 0)
        self.assertTrue(len(self.bisystem.orbits) == 1)
        self.assertTrue(len(self.trisystem.orbits) == 2)
        self.assertTrue(
            self.trisystem.orbits[1][0] > self.trisystem.orbits[0][0]
        )

    def test_min_max_separations(self):
        self.assertTrue(
            len(self.unisystem.orbits) ==
            len(self.unisystem.make_min_max_separations(self.unisystem.orbits))
        )
        self.assertTrue(
            len(self.bisystem.orbits) ==
            len(self.bisystem.make_min_max_separations(self.bisystem.orbits))
        )

        # Min and max separations can be equal for circular orbits
        bi_min_max = self.bisystem.make_min_max_separations(
            self.bisystem.orbits
        )
        self.assertTrue(bi_min_max[0][0] <= bi_min_max[0][1])

    def test_calc_forbidden_zones(self):
        bisystem_forbidden_zones = self.bisystem.calc_forbidden_zones(
            self.bisystem.minmax_separation
        )
        self.assertTrue(
            len(self.bisystem.minmax_separation) ==
            len(bisystem_forbidden_zones)
        )
        self.assertTrue(
            bisystem_forbidden_zones[0][0] < bisystem_forbidden_zones[0][1]
        )

    def test_periods(self):
        bisystem_periods = self.bisystem.make_periods(
            self.bisystem.stars,
            self.bisystem.orbits
        )
        self.assertTrue(len(bisystem_periods) == len(self.bisystem.orbits))
