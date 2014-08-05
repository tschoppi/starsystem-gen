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

    def makebbtemp(self, lum, orb):
        self.__bbtemp = 278 * lum**(0.25) * orb**(-0.5)

    def getBBTemp(self):
        return self.__bbtemp

    def getOrbit(self):
        return self.__orbit
