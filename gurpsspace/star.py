from . import dice as GD
from . import planetsystem as PS
from .tables import StEvoTable, IndexTable, SequenceTable


class Star:
    roller = GD.DiceRoller()

    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self, age):
        self.__hasforbiddenzone = False
        # roller = GD.DiceRoller()
        self.__age = age
        self.make_index()
        self.make_mass()
        self.find_sequence()
        self.make_luminosity()
        self.make_temperature()
        self.make_radius()
        self.compute_orbit_limits()
        self.compute_snow_line()

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

    def get_mass(self):
        return self.__mass

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age
        # Eventually some recalculations will have to be done

    def make_index(self):
        # Roll to randomly select the index for the StEvoTable
        diceroll1 = self.roll(3, 0)
        diceroll2 = self.roll(3, 0)
        self.__StEvoIndex = IndexTable[diceroll1][diceroll2]

    def make_mass(self):
        self.__mass = StEvoTable['mass'][self.__StEvoIndex]

    def find_sequence(self):
        # Check what sequences are available
        seq = StEvoTable['internaltype'][self.__StEvoIndex]
        age = self.__age

        # If we have a main-sequence-only star
        if seq == 0:
            self.__SeqIndex = 0

        # If we have a main-sequence-only star that can decay to a white dwarf
        elif seq == 1:
            span = StEvoTable['Mspan'][self.__StEvoIndex]
            if age > span:
                self.__SeqIndex = 3
            else:
                self.__SeqIndex = 0

        # If we have a star with sub- and giant type capabilities
        elif seq == 2:
            mspan = StEvoTable['Mspan'][self.__StEvoIndex]
            sspan = StEvoTable['Sspan'][self.__StEvoIndex]
            gspan = StEvoTable['Gspan'][self.__StEvoIndex]
            if age > (mspan + sspan + gspan):
                self.__SeqIndex = 3
            elif age > (mspan + sspan):
                self.__SeqIndex = 2
            elif age > mspan:
                self.__SeqIndex = 1
            else:
                self.__SeqIndex = 0
        # For a white dwarf we have to regenerate the mass
        if self.__SeqIndex == 3:
            self.__mass = self.roll(2, -2) * 0.05 + 0.9

    def get_sequence(self):
        return SequenceTable[self.__SeqIndex]

    def make_luminosity(self):
        seq = self.__SeqIndex
        age = self.__age
        lmin = StEvoTable['Lmin'][self.__StEvoIndex]
        lmax = StEvoTable['Lmax'][self.__StEvoIndex]
        mspan = StEvoTable['Mspan'][self.__StEvoIndex]
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

        self.__luminosity = lum

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
            temp = self.roll(2, -2) * 200 + 3000
        elif seq == 3:  # White dwarf
            temp = 8000  # Not defined in the rulebook, so arbitrarily assigned

        self.__temperature = temp

    def getTemp(self):
        return self.__temperature

    def make_radius(self):
        lum = self.__luminosity
        temp = self.__temperature
        rad = 155000 * lum ** 0.5 / temp ** 2
        if self.__SeqIndex == 3:  # If we're a white dwarf
            rad = 0.000043  # The size is comparable to the one of Earth

        self.__radius = rad

    def compute_orbit_limits(self):
        mass = self.__mass
        lum = self.__luminosity

        # Inner Orbital Limit
        inner1 = 0.1 * mass
        inner2 = 0.01 * lum ** 0.5
        if inner1 > inner2:
            self.__innerlimit = inner1
        else:
            self.__innerlimit = inner2

        # Outer Orbital Limit
        self.__outerlimit = 40 * mass

    def compute_snow_line(self):
        initlum = StEvoTable['Lmin'][self.__StEvoIndex]
        self.__snowline = 4.85 * initlum ** 0.5

    def set_forbidden_zone(self, inner, outer):
        self.__forbiddenzone = (inner, outer)
        self.__hasforbiddenzone = True

    def make_planetsystem(self):
        self.planetsystem = PS.PlanetSystem(self)

    def get_orbit_limits(self):
        return (self.__innerlimit, self.__outerlimit)

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
