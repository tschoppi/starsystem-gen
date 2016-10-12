from typing import Tuple

from . import dice


class OrbitContent:
    """
    Generic class for contents of orbits.
    """

    def __init__(self,
                 primary,    # Primary star
                 orbitalradius):
        self.roller = dice.DiceRoller()
        self.orbit = orbitalradius
        self.primary_star = primary
        primarylum = self.primary_star.get_luminosity()
        self.blackbody_temperature = self.make_blackbody_temperature(primarylum, self.orbit)
        self.period = self.make_orbital_period()
        self.name = ''
        self.number = None
        self.size = ''
        self.eccentricity = 0
        self.min_max = ()

    def make_blackbody_temperature(self, luminosity, orbit) -> float:
        return 278 * luminosity ** 0.25 * orbit ** -0.5

    def get_blackbody_temp(self) -> float:
        return self.blackbody_temperature

    def get_orbit(self) -> float:
        return self.orbit

    def make_orbital_period(self) -> float:
        m = self.primary_star.get_mass()
        return (self.orbit ** 3 / m) ** 0.5

    def get_period(self):
        return self.period

    def make_eccentricity(self, droll):
        """
        Determine eccentricity of orbit with the roll result.
        :param droll: Dice roll value
        """
        ecc = 0
        if droll > 3:
            ecc = 0.05
        if droll > 6:
            ecc = 0.1
        if droll > 9:
            ecc = 0.15
        if droll == 12:
            ecc = 0.2
        if droll == 13:
            ecc = 0.3
        if droll == 14:
            ecc = 0.4
        if droll == 15:
            ecc = 0.5
        if droll == 16:
            ecc = 0.6
        if droll == 17:
            ecc = 0.7
        if droll >= 18:
            ecc = 0.8
        return ecc

    def get_eccentricity(self):
        return self.eccentricity

    def make_min_max(self) -> Tuple[float, float]:
        min_orbit = self.get_orbit() * (1 - self.eccentricity)
        max_orbit = self.get_orbit() * (1 + self.eccentricity)
        return min_orbit, max_orbit

    def get_min_max(self) -> Tuple[float, float]:
        return self.min_max

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_angled_name(self):
        return "<" + self.name + ">"

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    # Overload in subclasses if applicable
    def get_type(self):
        return ''

    def get_size(self):
        return self.size

    def num_moons(self):
        return ''

    def num_moonlets(self):
        return ''
