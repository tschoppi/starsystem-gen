from .orbitcontents import OrbitContent
from .tables import WorldClimate


class AsteroidBelt(OrbitContent):
    """Class for asteroid belts."""
    def __init__(self, primarystar, orbitalradius):
        OrbitContent.__init__(self, primarystar, orbitalradius)
        self.makeresources()
        self.makesurftemp()
        self.makeclimate()
        self.__habitability = 0
        self.__affinity = self.__habitability + self.__rvm

    def __repr__(self):
        return repr("Asteroid Belt")

    def type(self):
        return "Ast. Belt"

    def printinfo(self):
        print("Asteroid Belt {}".format(self.getName()))
        print("    Orbit:\t{}".format(self.getOrbit()))
        print("  Orb Per:\t{}".format(self.getPeriod()))
        print("  Orb Ecc:\t{}".format(self.getEcc()))
        print("      RVM:\t{}".format(self.__rvm))
        print("   Res. V:\t{}".format(self.__resources))
        print("     Aff.:\t{}".format(self.__affinity))
        print("")

    def makeresources(self):
        dice = self.roll(3,0)
        rvm = -5
        value = 'Worthless'
        if dice == 4:
            rvm = -4
            value = 'Very Scant'
        if dice == 5:
            rvm = -3
            value = 'Scant'
        if dice >= 6 and dice <= 7:
            rvm = -2
            value = 'Very Poor'
        if dice >= 8 and dice <= 9:
            rvm = -1
            value = 'Poor'
        if dice >= 10 and dice <= 11:
            rvm = 0
            value = 'Average'
        if dice >= 12 and dice <= 13:
            rvm = 1
            value = 'Abundant'
        if dice >= 14 and dice <= 15:
            rvm = 2
            value = 'Very Abundant'
        if dice == 16:
            rvm = 3
            value = 'Rich'
        if dice == 17:
            rvm = 4
            value = 'Very Rich'
        if dice == 16:
            rvm = 5
            value = 'Motherlode'
        self.__rvm = rvm
        self.__resources = value

    def makesurftemp(self):
        self.__avsurf = self.getBBTemp() * 0.97

    def getAvSurf(self):
        return self.__avsurf

    def makeclimate(self):
        self.__climate = WorldClimate(self.getAvSurf())

    def getClimate(self):
        return self.__climate

    def getResources(self):
        return self.__resources

    def getRVM(self):
        return self.__rvm

    def getAffinity(self):
        return self.__affinity
