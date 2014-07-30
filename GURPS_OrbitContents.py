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
        self.generatemoons()

    def __repr__(self):
        return repr("{} Terrestrial Planet".format(self.getSize()))

    def type(self):
        return "Terrestrial World"

    def generatemoons(self):
        rollmod = -4
        rollmod += self.moonrollmodifier()
        moonroll = self.roll(1, rollmod)
        if moonroll < 0:
            moonroll = 0
            # If we have no major moons, generate moonlets
            self.generatemoonlets()
        self.__nummoons = moonroll
        self.__moons = [Moon(self) for moonnum in range(moonroll)]

    def generatemoonlets(self):
        rollmod = -2
        rollmod += self.moonrollmodifier()
        moonletroll = self.roll(1, rollmod)
        if moonletroll < 0:
            moonletroll = 0
        self.__nummoonlets = moonletroll
        self.__moonlets = [Moonlet(self) for moonletnum in range(moonletroll)]

    def moonrollmodifier(self):
        modifier = 0
        orbit = self.getOrbit()
        if orbit <= 0.5:
            return -20 # Equivalent to "do not roll"
        if orbit > 0.5 and orbit <= 0.75:
            modifier -= 3
        if orbit > 0.75 and orbit <= 1.5:
            modifier -= 1
        modifier += (SizeToInt[self.getSize()] - 2)
        return modifier

    def getSatellites(self):
        if self.__nummoons > 0:
            return self.__moons
        if self.__nummoonlets > 0:
            return self.__moonlets


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
    def __init__(self, parentplanet):
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
