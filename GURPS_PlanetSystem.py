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


    def allowedorbit(self, testorbit):
        result  = testorbit >= self.__innerlimit
        result &= testorbit <= self.__outerlimit
        if self.__forbidden and result:
            result2 = testorbit <= self.__innerforbidden
            result2 |= testorbit >= self.__outerforbidden
            return result & result2
        else:
            return result
