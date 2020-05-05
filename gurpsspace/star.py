from . import dice
from . import planetsystem
from .tables import StEvoTable, IndexTable, SequenceTable


class Star:
    roller = dice.DiceRoller()

    def __init__(self, age):
        if age <= 0:
            raise ValueError("Age needs to be a positive number.")

        self.__hasforbiddenzone = False
        self.__forbiddenzone = None
        self.__age = age
        self.__StEvoIndex = self.make_index()
        self.__SeqIndex = self.find_sequence()
        self.__mass = self.make_mass()
        self.__luminosity = self.make_luminosity()
        self.__temperature = self.make_temperature()
        self.__radius = self.make_radius()
        self.__innerlimit, self.__outerlimit = self.compute_orbit_limits()
        self.__snowline = self.compute_snow_line()
        self.__letter = 'A'
        self.__star_type = self.get_star_type()
        self.planetsystem = None

    def __repr__(self):
        return repr((self.__mass, self.__luminosity, self.__temperature))

    def print_info(self):
        print("  Star {} Info".format(self.__letter))
        print("  ---------")
        print("       Mass:\t{}".format(self.__mass))
        print("   Sequence:\t{}".format(SequenceTable[self.__SeqIndex]))
        print(" Luminosity:\t{}".format(self.__luminosity))
        print("Temperature:\t{}".format(self.__temperature))
        print("     Radius:\t{}".format(round(self.__radius, 6)))
        # print("       Type:\t{}".format(self.__type))

        # Nicely formatted orbital zone
        norzone = (round(self.__innerlimit, 3), round(self.__outerlimit, 3))
        print("Orbital Zne:\t{}".format(norzone))
        # Nicely formatted snow line
        nsnline = round(self.__snowline, 3)
        print("  Snow Line:\t{}".format(nsnline))
        if self.__hasforbiddenzone:
            # Nicely formatted forbidden zone
            nforb = [round(fz) for fz in self.__forbiddenzone]
            print(" Forbid Zne:\t{}".format(nforb))
        self.planetsystem.printinfo()
        print("  ---------\n")

    def get_mass(self) -> float:
        return self.__mass

    def get_age(self):
        return self.__age

    def make_index(self) -> int:
        # Roll to randomly select the index for the StEvoTable
        diceroll1 = self.roller.roll_dice(3, 0)
        diceroll2 = self.roller.roll_dice(3, 0)
        return IndexTable[diceroll1][diceroll2]

    def make_mass(self) -> float:
        """
        Find or calculate the mass appropriate to the star.
        :return: The mass of the star, relative to the sun.
        """
        if self.__SeqIndex == 3:  # The star is a white dwarf, and its mass is treated specially
            return self.roller.roll_dice(2, -2) * 0.05 + 0.9
        return StEvoTable['mass'][self.__StEvoIndex]

    def find_sequence(self) -> int:
        # Check what sequences are available
        seq = StEvoTable['internaltype'][self.__StEvoIndex]
        age = self.__age
        sequence_index = 0

        # If we have a main-sequence-only star that can decay to a white dwarf
        if seq == 1:
            span = StEvoTable['Mspan'][self.__StEvoIndex]
            if age > span:
                sequence_index = 3

        # If we have a star with sub- and giant type capabilities
        elif seq == 2:
            mspan = StEvoTable['Mspan'][self.__StEvoIndex]
            sspan = StEvoTable['Sspan'][self.__StEvoIndex]
            gspan = StEvoTable['Gspan'][self.__StEvoIndex]
            if age > (mspan + sspan + gspan):
                sequence_index = 3
            elif age > (mspan + sspan):
                sequence_index = 2
            elif age > mspan:
                sequence_index = 1
        return sequence_index

    def get_sequence(self) -> str:
        return SequenceTable[self.__SeqIndex]

    def make_luminosity(self):
        seq = self.__SeqIndex
        age = self.__age
        lmin = StEvoTable['Lmin'][self.__StEvoIndex]
        lmax = StEvoTable['Lmax'][self.__StEvoIndex]
        mspan = StEvoTable['Mspan'][self.__StEvoIndex]
        lum = 0
        if seq == 0:
            # For stars with no Mspan value (mspan == 0)
            if mspan == 0:
                lum = lmin
            else:
                lum = lmin + (age / mspan * (lmax - lmin))
        elif seq == 1:  # Subgiant star
            lum = lmax
        elif seq == 2:  # Giant star
            lum = 25 * lmax
        elif seq == 3:  # White dwarf
            lum = 0.001

        return lum

    def make_temperature(self):
        seq = self.__SeqIndex
        age = self.__age
        #  lmin = StEvoTable['Lmin'][self.__StEvoIndex]
        #  lmax = StEvoTable['Lmax'][self.__StEvoIndex]
        mspan = StEvoTable['Mspan'][self.__StEvoIndex]
        sspan = StEvoTable['Sspan'][self.__StEvoIndex]
        #  gspan = StEvoTable['Gspan'][self.__StEvoIndex]
        if seq == 0:
            temp = StEvoTable['temp'][self.__StEvoIndex]
        elif seq == 1:  # Subgiant star
            m = StEvoTable['temp'][self.__StEvoIndex]
            a = age - mspan
            s = sspan
            temp = m - (a / s * (m - 4800))
        elif seq == 2:  # Giant star
            temp = self.roller.roll_dice(2, -2) * 200 + 3000
        elif seq == 3:  # White dwarf
            temp = 8000  # Not defined in the rulebook, so arbitrarily assigned

        return temp

    def get_temp(self):
        return self.__temperature

    def make_radius(self):
        lum = self.__luminosity
        temp = self.__temperature
        rad = 155000 * lum ** 0.5 / temp ** 2
        if self.__SeqIndex == 3:  # If we're a white dwarf
            rad = 0.000043  # The size is comparable to the one of Earth

        return rad

    def compute_orbit_limits(self):
        mass = self.__mass
        lum = self.__luminosity

        # Inner Orbital Limit
        inner1 = 0.1 * mass
        inner2 = 0.01 * lum ** 0.5
        if inner1 > inner2:
            inner_limit = inner1
        else:
            inner_limit = inner2

        # Outer Orbital Limit
        outer_limit = 40 * mass
        return inner_limit, outer_limit

    def compute_snow_line(self):
        initlum = StEvoTable['Lmin'][self.__StEvoIndex]
        return 4.85 * initlum ** 0.5

    def set_forbidden_zone(self, inner, outer):
        if inner >= outer:
            raise ValueError("Inner limit must be smaller than outer limit.")
        self.__forbiddenzone = (inner, outer)
        self.__hasforbiddenzone = True

    def make_planetsystem(self):
        # TODO: Why not call this in the constructor and avoid this side effect too?
        self.planetsystem = planetsystem.PlanetSystem(self)

    def get_orbit_limits(self):
        return self.__innerlimit, self.__outerlimit

    def get_snowline(self):
        return self.__snowline

    def get_luminosity(self):
        return self.__luminosity

    def has_forbidden_zone(self):
        return self.__hasforbiddenzone

    def get_forbidden_zone(self):
        return self.__forbiddenzone

    def get_radius(self):
        return self.__radius

    def set_letter(self, letter):
        self.__letter = letter

    def get_letter(self):
        return self.__letter

    def get_star_type(self) -> str:
        """
        Get the star spectral type by the star temperature
        :return: Spectral Index
        """
        sp_index = min(range(len(StEvoTable['temp'])),
                       key=lambda i: abs(StEvoTable['temp'][i] - self.get_temp()))
        return StEvoTable['type'][sp_index]
