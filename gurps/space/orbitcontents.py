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
        self.primarystar = primary
        primarylum = self.primarystar.getLuminosity()
        self.makebbtemp(primarylum, self.__orbit)
        self.makeorbitperiod()

    def makebbtemp(self, lum, orb):
        self.__bbtemp = 278 * lum**(0.25) * orb**(-0.5)

    def getBBTemp(self):
        return self.__bbtemp

    def getOrbit(self):
        return self.__orbit

    def makeorbitperiod(self):
        m = self.primarystar.getMass()
        self.__period = (self.__orbit**3 / m)**(0.5)

    def getPeriod(self):
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

    def getEcc(self):
        if self.__eccset:
            return self.__ecc
        else:
            return None
