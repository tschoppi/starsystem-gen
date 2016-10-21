from . import dice
from . import planetsystem
from .tables import StEvoTable, IndexTable, SequenceTable


class Star:
    roller = dice.DiceRoller()

    def __init__(self, age):
        if age <= 0:
            raise ValueError("Age needs to be a positive number.")

        self.hasforbiddenzone = False
        self.forbiddenzone = None
        self.age = age
        self.stellar_evolution_index = self.make_index()
        self.sequence_index = self.find_sequence_index()
        self.mass = self.make_mass()
        self.luminosity = self.make_luminosity()
        self.temperature = self.make_temperature()
        self.radius = self.make_radius()
        self.innerlimit, self.outerlimit = self.compute_orbit_limits()
        self.snowline = self.compute_snow_line()
        self.letter = 'A'
        self.planetsystem = None

    def __repr__(self):
        return repr((self.mass, self.luminosity, self.temperature))

    def print_info(self) -> None:
        """Print information about Star to STDOUT"""
        print("  Star {} Info".format(self.letter))
        print("  ---------")
        print("       Mass:\t{}".format(self.mass))
        print("   Sequence:\t{}".format(SequenceTable[self.sequence_index]))
        print(" Luminosity:\t{}".format(self.luminosity))
        print("Temperature:\t{}".format(self.temperature))
        print("     Radius:\t{}".format(round(self.radius, 6)))
        # print("       Type:\t{}".format(self.__type))

        # Nicely formatted orbital zone
        norzone = (round(self.innerlimit, 3), round(self.outerlimit, 3))
        print("Orbital Zne:\t{}".format(norzone))
        # Nicely formatted snow line
        nsnline = round(self.snowline, 3)
        print("  Snow Line:\t{}".format(nsnline))
        if self.hasforbiddenzone:
            # Nicely formatted forbidden zone
            nforb = [round(fz) for fz in self.forbiddenzone]
            print(" Forbid Zne:\t{}".format(nforb))
        self.planetsystem.printinfo()
        print("  ---------\n")

    def get_mass(self) -> float:
        return self.mass

    def get_age(self) -> float:
        return self.age

    def make_index(self) -> int:
        """Roll to randomly select the index for the StEvoTable"""
        diceroll1 = self.roller.roll_dice(3, 0)
        diceroll2 = self.roller.roll_dice(3, 0)
        return IndexTable[diceroll1][diceroll2]

    def make_mass(self) -> float:
        """
        Find or calculate the mass appropriate to the star.

        :return: The mass of the star, relative to the sun.
        """
        if self.sequence_index == 3:  # The star is a white dwarf, and its mass is treated specially
            return self.roller.roll_dice(2, -2) * 0.05 + 0.9
        return StEvoTable['mass'][self.stellar_evolution_index]

    def find_sequence_index(self) -> int:
        # Check what sequences are available
        seq = StEvoTable['internaltype'][self.stellar_evolution_index]
        sequence_index = 0

        # If we have a main-sequence-only star that can decay to a white dwarf
        if seq == 1:
            span = StEvoTable['Mspan'][self.stellar_evolution_index]
            if self.age > span:
                sequence_index = 3

        # If we have a star with sub- and giant type capabilities
        elif seq == 2:
            mspan = StEvoTable['Mspan'][self.stellar_evolution_index]
            sspan = StEvoTable['Sspan'][self.stellar_evolution_index]
            gspan = StEvoTable['Gspan'][self.stellar_evolution_index]
            if self.age > (mspan + sspan + gspan):
                sequence_index = 3
            elif self.age > (mspan + sspan):
                sequence_index = 2
            elif self.age > mspan:
                sequence_index = 1
        return sequence_index

    def get_sequence(self) -> str:
        return SequenceTable[self.sequence_index]

    def make_luminosity(self) -> float:
        """
        Calculate the luminosity of the star

        :return: Luminosity relative to the Sun
        """
        lmin = StEvoTable['Lmin'][self.stellar_evolution_index]
        lmax = StEvoTable['Lmax'][self.stellar_evolution_index]
        mspan = StEvoTable['Mspan'][self.stellar_evolution_index]
        luminosity = 0
        if self.sequence_index == 0:
            # For stars with no Mspan value (mspan == 0)
            if mspan == 0:
                luminosity = lmin
            else:
                luminosity = lmin + (self.age / mspan * (lmax - lmin))
        elif self.sequence_index == 1:  # Subgiant star
            luminosity = lmax
        elif self.sequence_index == 2:  # Giant star
            luminosity = 25 * lmax
        elif self.sequence_index == 3:  # White dwarf
            luminosity = 0.001
        return luminosity

    def make_temperature(self) -> float:
        """
        Calculate the temperature of the star

        :return: Temperature of the star, in Kelvin
        """
        mspan = StEvoTable['Mspan'][self.stellar_evolution_index]
        sspan = StEvoTable['Sspan'][self.stellar_evolution_index]
        if self.sequence_index == 0:
            temperature = StEvoTable['temp'][self.stellar_evolution_index]
        elif self.sequence_index == 1:  # Subgiant star
            m = StEvoTable['temp'][self.stellar_evolution_index]
            a = self.age - mspan
            s = sspan
            temperature = m - (a / s * (m - 4800))
        elif self.sequence_index == 2:  # Giant star
            temperature = self.roller.roll_dice(2, -2) * 200 + 3000
        elif self.sequence_index == 3:  # White dwarf
            # For white dwarves the temperature is arbitrarily assigned
            temperature = 8000
        return temperature

    def get_temp(self) -> float:
        """Get temperature of the star"""
        return self.temperature

    def make_radius(self) -> float:
        """
        Calculate the apparent radius of the star

        :return: Radius of the star, relative to the Sun
        """
        lum = self.luminosity
        temp = self.temperature
        rad = 155000 * lum ** 0.5 / temp ** 2
        if self.sequence_index == 3:  # If we're a white dwarf
            rad = 0.000043  # The size is comparable to the one of Earth
        return rad

    def compute_orbit_limits(self) -> list:
        """
        Calculate the limits for safe orbits around the star

        :return: List of two floats for inner and outer limit, respectively
        """
        # Inner Orbital Limit
        inner1 = 0.1 * self.mass
        inner2 = 0.01 * self.luminosity ** 0.5
        inner_limit = max(inner1, inner2)

        # Outer Orbital Limit
        outer_limit = 40 * self.mass
        return inner_limit, outer_limit

    def compute_snow_line(self) -> float:
        """
        Calculate the snow line for this star

        :return: Snow line in AU
        """
        initial_luminosity = StEvoTable['Lmin'][self.stellar_evolution_index]
        return 4.85 * initial_luminosity ** 0.5

    def set_forbidden_zone(self, inner, outer) -> None:
        """
        Set the forbidden zone around this star

        :param inner: Inner limit of the forbidden zone
        :param outer: Outer limit of the forbidden zone
        :type inner: float
        :type outer: float

        The forbidden zone is a zone where no stable orbits can exist due to the
        gravitational pull of other stars in the same star system. These values
        can only be calculated with knowledge of the other stars in mind, and
        thus has to be done by the StarSystem. The forbidden zone limits are
        then communicated to the Stars, if necessary.
        """
        if inner >= outer:
            raise ValueError("Inner limit must be smaller than outer limit.")
        self.forbiddenzone = (inner, outer)
        self.hasforbiddenzone = True

    def make_planetsystem(self) -> None:
        # TODO: Why not call this in the constructor and avoid this side effect too?
        self.planetsystem = planetsystem.PlanetSystem(self)

    def get_orbit_limits(self) -> list:
        """Get inner and outer orbit limits around this star, in a list"""
        return self.innerlimit, self.outerlimit

    def get_snowline(self) -> float:
        """Get snowline in AU around this star"""
        return self.snowline

    def get_luminosity(self) -> float:
        """Get the luminosity of this star, relative to the Sun"""
        return self.luminosity

    def has_forbidden_zone(self) -> bool:
        """Returns True for a star with a forbidden zone set"""
        return self.hasforbiddenzone

    def get_forbidden_zone(self) -> tuple:
        """Returns tuple (inner, outer) limits of the forbidden zone"""
        return self.forbiddenzone

    def get_radius(self) -> float:
        """Return the radius, relative to the Sun"""
        return self.radius

    def set_letter(self, letter) -> None:
        """Set the name of the star

        :param letter: Letter to assign to the star
        :type letter: char
        """
        self.letter = letter

    def get_letter(self):
        """Returns letter of the star"""
        return self.letter
