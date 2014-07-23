# Here live all the GURPS Orbit Contents; Planets and Asteroid Belts
import GURPS_Dice as GD

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

class World(OrbitContent):
    pass
#class TerrPlanet(Planet):

class AsteroidBelt(OrbitContent):
    pass

class GasGiant(OrbitContent):
    def __init__(self, primarylum, orbitalradius, snowline, rollbonus=True):
        OrbitContent.__init__(self, primarylum, orbitalradius)
        self.makesize(rollbonus)
        self.printinfo()

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

    def printinfo(self):
        print("Gas Giant Properties")
        print("--------------------")
        print("   Size:\t{}".format(self.__size))
        print("BB Temp:\t{}".format(self.getBBTemp()))
        print("--------------------")
