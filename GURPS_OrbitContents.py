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
    pass
