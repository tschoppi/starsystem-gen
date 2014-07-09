import GURPS_Dice as GD
from GURPS_Tables import StEvoTable, IndexTable

class Star:
    roller = GD.DiceRoller()

    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self, age):
        roller = GD.DiceRoller()
        self.setAge(age)
        self.makeindex()
        self.makemass()
        self.printinfo()

    def printinfo(self):
        print("  Star Info")
        print("  ---------")
        #print("        Age:\t{}".format(self.__age))
        print("       Mass:\t{}".format(self.__mass))
        #print("       Type:\t{}".format(self.__type))
        print("  ---------\n")

    def getMass(self):
        return self.__mass

    def getAge(self):
        return self.__age

    def setAge(self, age):
        self.__age = age

    def makeindex(self):
        # Roll to randomly select the index for the StEvoTable
        diceroll1 = self.roll(3, 0)
        diceroll2 = self.roll(3, 0)
        self.__StEvoIndex = IndexTable[diceroll1][diceroll2]

    def makemass(self):
        self.__mass = StEvoTable['mass'][self.__StEvoIndex]
