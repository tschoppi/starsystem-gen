from . import dice as GD

class OrbitContent:
    """Generic class for contents of orbits."""
    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self,
                 primary,    # Primary star
                 orbitalradius):
        self.roller = GD.DiceRoller()
        self.__orbit = orbitalradius
        self.primary_star = primary
        primarylum = self.primary_star.get_luminosity()
        self.make_blackbody_temperature(primarylum, self.__orbit)
        self.makeorbitperiod()

    def make_blackbody_temperature(self, lum, orb):
        self.__bbtemp = 278 * lum**(0.25) * orb**(-0.5)

    def get_blackbody_temp(self):
        return self.__bbtemp

    def get_orbit(self):
        return self.__orbit

    def makeorbitperiod(self):
        m = self.primary_star.get_mass()
        self.__period = (self.__orbit**3 / m)**(0.5)

    def get_period(self):
        return self.__period

    def seteccentricity(self, droll):
        """Determine eccentricity of orbit with the roll result."""
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
        self.__ecc = ecc
        self.__eccset = True
        self.makeminmax()

    def get_eccentricity(self):
        if self.__eccset:
            return self.__ecc
        else:
            return None

    def makeminmax(self):
        min = self.get_orbit() * (1 - self.__ecc)
        max = self.get_orbit() * (1 + self.__ecc)
        self.__minmax = (min, max)

    def getMinMax(self):
        return self.__minmax

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_number(self, number):
        self.__number = number

    def getNumber(self):
        return self.__number

    # Overload in subclasses if applicable
    def get_type(self):
        return ''
    def get_size(self):
        return ''
    def num_moons(self):
        return ''
    def num_moonlets(self):
        return ''
