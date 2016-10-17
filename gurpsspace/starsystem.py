from . import star
from . import dice
from .tables import OrbSepTable, StOEccTable
from .output import latexout
LW = latexout.LatexWriter


class StarSystem:
    roller = dice.DiceRoller()

    def __init__(self, **kwargs):
        open_cluster = kwargs.get('open_cluster', None)
        self.opencluster = self.make_open_cluster(open_cluster)
        num_stars = kwargs.get('num_stars', None)
        self.num_stars = self.make_number_of_stars(num_stars)
        age = kwargs.get('age', None)
        self.age = self.make_age(age)
        self.stars = self.generate_stars(self.num_stars)
        self.stars = sorted(
            self.stars, key=lambda star: star.get_mass(), reverse=True
        )
        self.stars = self.name_stars(self.stars)
        self.orbits = self.make_orbits()
        self.minmax_separation = self.make_min_max_separations(self.orbits)
        self.forbidden_zones = self.calc_forbidden_zones(self.minmax_separation)
        self.stars = self.propagate_forbidden_zones(
            self.stars,
            self.forbidden_zones
        )
        self.stars = self.create_planetsystem(self.stars)
        self.periods = self.make_periods(self.stars, self.orbits)

    def print_info(self) -> None:
        """
        Outputs all information about the starsystem to console.
        """
        print("Star System Info")
        print("================")
        print("        Age:\t{}".format(self.age))
        print(" # of Stars:\t{}".format(len(self.stars)))
        print("OpenCluster:\t{}".format(self.opencluster))
        if len(self.stars) > 1:
            print("Stellar Orb:\t{}".format(self.orbits))
            print("StOrbMinMax:\t{}".format(self.minmax_separation))
            print(" Orbit Per.:\t{}".format(self.periods))
        print("================\n")
        for i in range(len(self.stars)):
            self.stars[i].print_info()

    def make_open_cluster(self, kwarg) -> bool:
        """
        Decide whether the star system is in an open cluster

        :param kwarg: Keyword argument passed to the constructor
        :type kwarg: bool or None
        :return: True if the star system is in an open cluster, false otherwise
        """
        if kwarg is not None:
            return kwarg
        else:
            return self.random_cluster()

    def random_cluster(self) -> bool:
        """
        Randomly determines whether the star system is in an open cluster.

        :return: True if the system is in an open cluster.
        """
        # Criteria for a success (star system in an open cluster):
        #    - Roll of 10 or less
        return self.roller.roll_dice(3, 0) <= 10

    def make_number_of_stars(self, kwarg) -> int:
        """
        Determine number of stars in the star system

        :param kwarg: Keyword argument num_stars passed to constructor
        :type kwarg: int or None
        :return: Integer number of stars in the system

        According to the rules only 1-3 stars can be in any stellar system. This
        method does bounds checking and provides a random number of stars should
        that fail.
        """
        if kwarg is not None and 1 <= kwarg <= 3:
            return kwarg
        else:
            return self.random_star_number()

    def random_star_number(self) -> int:
        """
        Randomly determines the number of stars in the system.

        :return: The number of stars
        """
        if self.opencluster:
            roll_mod = 3
        else:
            roll_mod = 0
        dice_roll = self.roller.roll_dice(3, roll_mod)

        if dice_roll >= 16:
            return 3
        elif dice_roll <= 10:
            return 1
        else:
            return 2

    def generate_stars(self, number_of_stars) -> list:
        """
        Initialize the correct number of stars

        :param number_of_stars: The number of stars that need to be generated
        :type number_of_stars: int
        :return: A list with the stars
        """
        temporary_stars = []
        for i in range(number_of_stars):
            temporary_stars.append(star.Star(age=self.age))
        return temporary_stars

    def make_age(self, age=None) -> float:
        if age is None:
            provage = self.random_age()
            while self.opencluster and provage > 2:
                provage = self.random_age()
            return provage
        elif age <= 0:
            raise ValueError(
                "Starsystem age needs to be larger than zero billion years."
            )
        else:
            return age

    def random_age(self) -> float:
        """
        Randomly determines the age of the star system in billions of years.

        :return: A float factor of billion years.
        """
        dice_roll = self.roller.roll_dice(3, 0)
        if dice_roll == 3:
            # Extreme Population I: Age is set to 1 million years
            return 0.001
        elif dice_roll <= 6:
            return (
                0.1 + self.roller.roll_dice(1, -1) * 0.3 +
                self.roller.roll_dice(1, -1) * 0.05
            )
        elif dice_roll <= 10:
            return (
                2.0 + self.roller.roll_dice(1, -1) * 0.6 +
                self.roller.roll_dice(1, -1) * 0.1
            )
        elif dice_roll <= 14:
            return (
                5.6 + self.roller.roll_dice(1, -1) * 0.6 +
                self.roller.roll_dice(1, -1) * 0.1
            )
        elif dice_roll <= 17:
            return (
                8.0 + self.roller.roll_dice(1, -1) * 0.6 +
                self.roller.roll_dice(1, -1) * 0.1
            )
        else:
            return (
                10 + self.roller.roll_dice(1, -1) * 0.6 +
                self.roller.roll_dice(1, -1) * 0.1
            )

    def name_stars(self, starlist) -> list:
        """
        Assign a letter to each star

        :param starlist: List of the stars to name
        :type starlist: list
        :return: List of renamed stars

        The naming convention starts with the first (highest mass) star and the
        first letter of the alphabet.
        """
        letters = ['A', 'B', 'C']
        for star_ in starlist:
            star_.set_letter(letters[starlist.index(star_)])
        return starlist

    # TODO: Sub-companion star for distant second companion star
    def make_orbits(self) -> list:
        """
        Generate stellar orbits for multiple-star systems.

        :return: A list of orbits, the entries are of the form
            [orbital_separation, eccentricity]
        """
        orbsepentry = []
        orbits = []
        if len(self.stars) == 1:
            return orbits
        if len(self.stars) >= 2:
            dice = self.roller.roll_dice(3, 0)
            osepindex = self.find_orbital_separation_index(dice)
            orbsep = OrbSepTable[osepindex]
            orbit = self.roller.roll_dice(2, 0) * orbsep[1]

            eccmod = orbsep[2]
            eccroll = self.roller.roll_dice(3, eccmod)
            if eccroll < 3:
                eccroll = 3
            if eccroll > 18:
                eccroll = 18
            eccentricity = StOEccTable[eccroll]

            orbsepentry.append(orbsep)
            orbits.append((orbit, eccentricity))
        if len(self.stars) == 3:
            if osepindex == 4:
                # Disallow two 'Distant' companions
                return self.make_orbits()
            close_companion = True
            while close_companion:
                dice = self.roller.roll_dice(3, 6)
                osepindex = self.find_orbital_separation_index(dice)
                orbsep = OrbSepTable[osepindex]
                orbit = self.roller.roll_dice(2, 0) * orbsep[1]

                # The second companion star has to be further away than the
                # first companion star. Both the orbital modifier and orbit
                # values need to differ
                if orbsepentry[0][1] > orbsep[1] or orbits[0][0] >= orbit:
                    continue
                else:
                    close_companion = False

                eccmod = orbsep[2]
                eccroll = self.roller.roll_dice(3, eccmod)
                if eccroll < 3:
                    eccroll = 3
                if eccroll > 18:
                    eccroll = 18
                eccentricity = StOEccTable[eccroll]

                orbits.append((orbit, eccentricity))
        return orbits

    def find_orbital_separation_index(self, dice_roll) -> int:
        """
        Return index for the orbital separation table for a given dice roll

        :param dice_roll: Result of the dice roll
        :type dice_roll: int
        :return: An int in the interval [1, 4]
        """
        if dice_roll < 3:
            raise ValueError("The dice result should be >= 3")
        if dice_roll <= 6:
            return 0
        if dice_roll <= 9:
            return 1
        if dice_roll <= 11:
            return 2
        if dice_roll <= 14:
            return 3
        else:
            return 4

    def make_min_max_separations(self, orbits) -> list:
        """
        Calculate the minimal and maximal separations of multiple stars given
        their basic orbital parameters

        :param orbits: List of tuples (orbital_separation, eccentricity)
        :type orbits: list
        :return: List of tuples of the form (min, max) for each orbit entry
        """
        minmaxorbits = []
        for i in range(len(orbits)):
            orbit, ecc = orbits[i]
            min = (1 - ecc) * orbit
            max = (1 + ecc) * orbit
            minmaxorbits.append((min, max))
        return minmaxorbits

    def calc_forbidden_zones(self, minmax_separation) -> list:
        """
        Calculate the forbidden zones given minimal and maximal separations

        :param minmax_separation: List of tuples (min-, max-) orbital
            separations
        :type minmax_separation: list
        :return: List tuples with the forbidden zone edges (inner, outer)
        """
        forbiddenzones = []
        for i in range(len(minmax_separation)):
            min_, max_ = minmax_separation[i]
            start = min_ / 3.
            end = max_ * 3.
            forbiddenzones.append((start, end))
        return forbiddenzones

    def propagate_forbidden_zones(self, stars, forbidden_zones) -> list:
        """
        Set the forbidden zones for the stars

        :param stars: List of stars in the system
        :param forbidden_zones: List of tuples with forbidden zone edges
        :type stars: list
        :type forbidden_zones: list
        :return: List of stars with the forbidden zones set
        """
        for i in range(len(forbidden_zones)):
            start, end = forbidden_zones[i]
            if i == 0:  # For the first two stars
                stars[0].set_forbidden_zone(start, end)
                stars[1].set_forbidden_zone(start, end)
            if i == 1:  # For the third star
                stars[2].set_forbidden_zone(start, end)
        return stars

    def create_planetsystem(self, stars) -> list:
        """
        Let each star generate their planet system. It may be empty!

        :param stars: List of stars in the stellar system
        :type stars: list
        :return: List of stars that have planetary systems
        """
        for star_ in stars:
            star_.make_planetsystem()
        return stars

    def make_periods(self, stars, orbits):
        """
        Calculate the orbital periods for the stars

        :param stars: List of the stars
        :param orbits: List of tuples for orbital separation and eccentricity
        :type stars: list
        :type orbits: list
        :return: List of orbital periods in days
        """
        periods = []
        if len(stars) >= 2:
            orbit, ecc = orbits[0]
            m1 = stars[0].get_mass()
            m2 = stars[1].get_mass()
            m = m1 + m2
            periods.append((orbit ** 3 / m) ** 0.5)
        if len(stars) == 3:
            orbit, ecc = orbits[1]
            m1 = stars[0].get_mass() + stars[1].get_mass()
            m2 = stars[2].get_mass()
            m = m1 + m2
            periods.append((orbit ** 3 / m) ** 0.5)
        return periods

    def write_latex(self, filename='starsystem.tex') -> None:
        """
        Write all information about the starsystem to a latex file.

        :param filename: Name of file (with the .tex extension) to which the
            ouput is written
        :type filename: str
        """
        writer = LW(self, filename)
        writer.write()

    def get_age(self) -> int:
        """Return star system age in billion years"""
        return self.age

    def get_orbits(self) -> list:
        """
        Return list of tuples of the form (orbital separation, eccentricity).
        """
        return self.orbits

    def get_period(self) -> list:
        """Return list of orbital periods"""
        return self.periods

    def is_open_cluster(self) -> bool:
        """Return True if star system is located in an open cluster"""
        return self.opencluster

    def has_garden(self) -> bool:
        """
        Query all stars in the system for a Garden world

        :return: True if at least one star has a Garden world
        """
        ret = False
        for star_ in self.stars:
            ret |= star_.planetsystem.has_garden()
        return ret
