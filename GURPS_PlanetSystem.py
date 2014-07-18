import GURPS_Dice as GD

class PlanetSystem:
    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self, innerlimit, outerlimit, snowline,
                 innerforbidden=None, outerforbidden=None):
        self.roller = GD.DiceRoller()
        self.__innerlimit = innerlimit
        self.__outerlimit = outerlimit
        self.__snowline = snowline
        self.__forbidden = False
        if innerforbidden is not None and outerforbidden is not None:
            self.__innerforbidden = innerforbidden
            self.__outerforbidden = outerforbidden
            self.__forbidden = True
        self.makegasgiantarrangement()
        self.placegasgiant()
        self.createorbits()

    def printinfo(self):
        print("--------------------")
        print(" Planet System Info ")
        print("--------------------")
        print("GG Arrngmnt:\t{}".format(self.__gasarrangement))
        print("Frst GG Orb:\t{}".format(self.__firstgasorbit))
        print("     Orbits:\t{}".format(self.__orbitarray))

    def allowedorbit(self, testorbit):
        result  = testorbit >= self.__innerlimit
        result &= testorbit <= self.__outerlimit
        if self.__forbidden and result:
            result2 = testorbit <= self.__innerforbidden
            result2 |= testorbit >= self.__outerforbidden
            return result & result2
        else:
            return result

    def makegasgiantarrangement(self):
        dice = self.roll(3,0)
        self.__gasarrangement = 'None'
        if dice > 10:
            self.__gasarrangement = 'Conventional'
        if dice > 12:
            self.__gasarrangement = 'Eccentric'
        if dice > 14:
            self.__gasarrangement = 'Epistellar'

    def placegasgiant(self):
        orbit = 0
        if self.__gasarrangement == 'Conventional':
            orbit = (1 + (self.roll(2,-2) * 0.05)) * self.__snowline
        if self.__gasarrangement == 'Eccentric':
            orbit = self.roll(1,0) * 0.125 * self.__snowline
        if self.__gasarrangement == 'Epistellar':
            orbit = self.roll(3,0) * 0.1 * self.__innerlimit
        self.__firstgasorbit = orbit


    def createorbits(self):
        self.__orbitarray = []
