from . import star
from . import dice
from .tables import OrbSepTable, StOEccTable
from .output import latexout
LW = latexout.LatexWriter


class StarSystem:
    roller = dice.DiceRoller()

    def __init__(self, **kwargs):
        open_cluster = kwargs.get('open_cluster', None)

        if open_cluster is not None:
            self.__opencluster = open_cluster
        else:
            self.__opencluster = self.random_cluster()

        num_stars = kwargs.get('num_stars', None)
        if num_stars is not None:
            # The rules only support 1-3 stars per system, so it is checked whether the argument is valid.
            if 0 < num_stars <= 3:
                self.__numstars = num_stars
            else:  # Otherwise it is replaced with a random valid number.
                self.__numstars = self.random_star_number()
        else:
            self.__numstars = self.random_star_number()

        age = kwargs.get('age', None)
        self.make_age(age)
        self.generate_stars()
        self.sortstars()
        self.name_stars()
        self.make_orbits()
        self.make_min_max_separations()
        self.make_forbidden_zones()
        self.create_planetsystem()
        self.make_periods()
        # self.print_info()

    def printinfo(self) -> None:
        """
        Outputs all information about the starsystem to console.
        """
        print("Star System Info")
        print("================")
        print("        Age:\t{}".format(self.__age))
        print(" # of Stars:\t{}".format(self.__numstars))
        print("OpenCluster:\t{}".format(self.__opencluster))
        if self.__numstars > 1:
            print("Stellar Orb:\t{}".format(self.__orbits))
            print("StOrbMinMax:\t{}".format(self.__minmaxorbits))
            print(" Orbit Per.:\t{}".format(self.__periods))
        print("================\n")
        for i in range(self.__numstars):
            self.stars[i].print_info()

    def random_cluster(self) -> bool:
        """
        Randomly determines whether the star system is in an open cluster.
        :return: True if the system is in an open cluster.
        """
        # Criteria for a success (star system in an open cluster):
        #    - Roll of 10 or less
        return self.roller.roll_dice(3, 0) <= 10

    def random_star_number(self) -> int:
        """
        Randomly determines the number of stars in the system.
        :return: The number of stars
        """
        if self.__opencluster:
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

    def generate_stars(self) -> None:
        self.stars = []
        for i in range(self.__numstars):
            self.stars.append(star.Star(age=self.__age))

    def make_age(self, age) -> None:
        if age is None:
            provage = self.random_age()
            while self.__opencluster and provage > 2:
                provage = self.random_age()
            self.__age = provage
        else:
            self.__age = age

    def random_age(self) -> int:
        """
        Randomly determines the age of the star system in billions of years.
        :return: An int factor of billion years.
        """
        dice_roll = self.roller.roll_dice(3, 0)
        if dice_roll == 3:
            # Extreme Population I: Age is set to 1 million years
            return 0.001
        elif dice_roll <= 6:
            return 0.1 + self.roller.roll_dice(1, -1) * 0.3 + self.roller.roll_dice(1, -1) * 0.05
        elif dice_roll <= 10:
            return 2.0 + self.roller.roll_dice(1, -1) * 0.6 + self.roller.roll_dice(1, -1) * 0.1
        elif dice_roll <= 14:
            return 5.6 + self.roller.roll_dice(1, -1) * 0.6 + self.roller.roll_dice(1, -1) * 0.1
        elif dice_roll <= 17:
            return 8.0 + self.roller.roll_dice(1, -1) * 0.6 + self.roller.roll_dice(1, -1) * 0.1
        else:
            return 10 + self.roller.roll_dice(1, -1) * 0.6 + self.roller.roll_dice(1, -1) * 0.1

    def sortstars(self) -> None:
        """
        Sort the stars according to mass. Higher mass is placed first.
        """
        num = self.__numstars
        newlist = []
        for i in range(num):
            highest = 0    # Index of the star with the highest mass, reset to 0
            for j in range(len(self.stars)):
                if self.stars[highest].get_mass() < self.stars[j].get_mass():
                    highest = j
            newlist.append(self.stars[highest])
            del self.stars[highest]

        self.stars = newlist

    def name_stars(self) -> None:
        """
        Assign a letter to each star according to it's cardinality in the stellar system.
        """
        letters = ['A', 'B', 'C']
        for star_ in self.stars:
            star_.set_letter(letters[self.stars.index(star_)])

    # TODO: Sub-companion star for distant second companion star
    # TODO: Complete type-hinting, once the returns have been sorted out
    def make_orbits(self):
        """
        Generate stellar orbits for multiple-star systems.
        :return:
        """
        # FIXME: This looks like it shouldn't return anything, but it has two return statements!
        self.__orbsepentry = []
        self.__orbits = []
        if self.__numstars == 1:
            # Don't do anything for just one star
            return None
        if self.__numstars >= 2:
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

            self.__orbsepentry.append(orbsep)
            self.__orbits.append((orbit, eccentricity))
        if self.__numstars == 3:
            dice = self.roller.roll_dice(3, 6)
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

            self.__orbsepentry.append(orbsep)
            self.__orbits.append((orbit, eccentricity))

            # Recursively contine until second companion is significantly
            # further away than the first
            if self.__orbsepentry[0][1] >= self.__orbsepentry[1][1]:
                return self.make_orbits()

    def find_orbital_separation_index(self, dice_roll) -> int:
        # TODO: This needs a proper description
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

    def make_min_max_separations(self) -> None:
        self.__minmaxorbits = []
        for i in range(len(self.__orbits)):
            orbit, ecc = self.__orbits[i]
            min = (1 - ecc) * orbit
            max = (1 + ecc) * orbit
            self.__minmaxorbits.append((min, max))

    def make_forbidden_zones(self) -> None:
        self.__forbiddenzones = []
        for i in range(len(self.__minmaxorbits)):
            min_, max_ = self.__minmaxorbits[i]
            start = min_ / 3.
            end = max_ * 3.
            self.__forbiddenzones.append((start, end))

            # Tell the stars their forbidden zones
            if i == 0:  # For the first two stars
                self.stars[0].set_forbidden_zone(start, end)
                self.stars[1].set_forbidden_zone(start, end)
            if i == 1:  # For the third star
                self.stars[2].set_forbidden_zone(start, end)

    def create_planetsystem(self) -> None:
        """
        Causes all stars to generate a planetary system for themselves. These may be empty!
        """
        for star_ in self.stars:
            star_.make_planetsystem()

    def make_periods(self):
        self.__periods = []
        if self.__numstars >= 2:
            orbit, ecc = self.__orbits[0]
            m1 = self.stars[0].get_mass()
            m2 = self.stars[1].get_mass()
            m = m1 + m2
            self.__periods.append((orbit ** 3 / m) ** 0.5)
        if self.__numstars == 3:
            orbit, ecc = self.__orbits[1]
            m1 = self.stars[0].get_mass() + self.stars[1].get_mass()
            m2 = self.stars[2].get_mass()
            m = m1 + m2
            self.__periods.append((orbit ** 3 / m) ** 0.5)

    def write_latex(self) -> None:
        """
        Write all information about the starsystem to a latex file.
        """
        # FIXME: This is a hard-coded dependency on console input, which needs to be removed for use with a GUI.
        filename = input("Name of the file (include extension): ")
        if filename == '':
            writer = LW(self)
        else:
            writer = LW(self, filename)
        writer.write()

    def get_age(self) -> int:
        return self.__age

    def get_orbits(self):
        """
        Return tuple (orbital separation, eccentricity).
        """
        return self.__orbits

    def get_period(self):
        return self.__periods

    def is_open_cluster(self) -> bool:
        return self.__opencluster

    def has_garden(self) -> bool:
        ret = False
        for star_ in self.stars:
            ret |= star_.planetsystem.has_garden()
        return ret
