# Here live all the GURPS Orbit Contents; Planets and Asteroid Belts, Moons and
# Moonlets
import GURPS_Dice as GD
from GURPS_Tables import SizeToInt, IntToSize

class OrbitContent:
    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self,
                 primarylum,    # Primary star's luminosity
                 orbitalradius):
        self.roller = GD.DiceRoller()
        self.__orbit = orbitalradius
        self.makebbtemp(primarylum, self.__orbit)

    def makebbtemp(self, lum, orb):
        self.__bbtemp = 278 * lum**(0.25) * orb**(-0.5)

    def getBBTemp(self):
        return self.__bbtemp

    def getOrbit(self):
        return self.__orbit

class World(OrbitContent):
    def __init__(self, primarylum, orbitalradius, sizeclass):
        OrbitContent.__init__(self, primarylum, orbitalradius)
        self.__sizeclass = sizeclass

    def __repr__(self):
        return repr("World")

    def type(self):
        return "World"

    def getSize(self):
        return self.__sizeclass

class Planet(World):
    def __init__(self, primarylum, orbitalradius, sizeclass):
        World.__init__(self, primarylum, orbitalradius, sizeclass)

    def __repr__(self):
        return repr("{} Terrestrial Planet".format(self.getSize()))

    def type(self):
        return "Terrestrial World"

class AsteroidBelt(OrbitContent):
    def __repr__(self):
        return repr("Asteroid Belt")

    def type(self):
        return "Asteroid Belt"
    pass

class GasGiant(OrbitContent):
    def __init__(self, primarylum, orbitalradius, snowline, rollbonus=True):
        OrbitContent.__init__(self, primarylum, orbitalradius)
        self.makesize(rollbonus)
        #self.printinfo()

    def __repr__(self):
        return repr("{} Gas Giant".format(self.__size))

    def makesize(self, rollbonus):
        if rollbonus:
            modifier = 4
        else:
            modifier = 0
        dice = self.roll(3, modifier)
        self.__size = "Small"
        if dice > 10:
            self.__size = "Medium"
        if dice > 16:
            self.__size = "Large"

    def getSize(self):
        return self.__size

    def printinfo(self):
        print("Gas Giant Properties")
        print("--------------------")
        print("   Size:\t{}".format(self.__size))
        print("BB Temp:\t{}".format(self.getBBTemp()))
        print("--------------------")

    def type(self):
        return "Gas Giant"

class Moon(World):
    def __init__(self, primarylum, orbitalradius, sizeclass, parentplanet):
        self.parent = parentplanet
        self.makesize()

    def printinfo(self):
        print("Moon Information")
        print("Parent Planet:\t{}".format(self.parent))
        print("   Size Class:\t{}".format(self.__sizeclass))

    def makesize(self):
        parentsize = SizeToInt[parent.getSize()]
        if parent.type() == "Gas Giant":
            parentsize = SizeToInt["Large"]
        diceroll = self.roll(3,0)
        if diceroll >= 15:
            childsize = parentsize - 1
        if diceroll >= 12:
            childsize = parentsize - 2
        else:
            childsize = parentsize - 3
        if childsize < 0:
            childsize = 0
        self.__sizeclass = IntToSize[childsize]

class Moonlet:
    def roll(self, ndice, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self, parentplanet):
        self.parent = parentplanet
        self.roller = GD.DiceRoller()

    def printinfo(self):
        print("Moonlet Information")
        print("Parent Planet:\t{}".format(self.parent))
