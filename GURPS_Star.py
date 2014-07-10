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
        # Eventually some recalculations will have to be done

    def makeindex(self):
        # Roll to randomly select the index for the StEvoTable
        diceroll1 = self.roll(3, 0)
        diceroll2 = self.roll(3, 0)
        self.__StEvoIndex = IndexTable[diceroll1][diceroll2]

    def makemass(self):
        self.__mass = StEvoTable['mass'][self.__StEvoIndex]

    def findsequence(self):
        # Check what sequences are available
        seq = StEvoTable['internaltype'][self.__StEvoIndex]
        age = self.__age

        # If we have a main-sequence-only star
        if seq == 0:
            self.__SeqIndex = 0

        # If we have a main-sequence-only star that can decay to a white dwarf
        elif seq == 1:
            span = StEvoTable['Mspan'][self.__StEvoIndex]
            if age > span:
                self.__SeqIndex = 3
            else:
                self.__SeqIndex = 0

        # If we have a star with sub- and giant type capabilities
        elif seq == 2:
            mspan = StEvoTable['Mspan'][self.__StEvoIndex]
            sspan = StEvoTable['Sspan'][self.__StEvoIndex]
            gspan = StEvoTable['Gspan'][self.__StEvoIndex]
            if age > gspan:
                self.__SeqIndex = 3
            elif age > sspan:
                self.__SeqIndex = 2
            elif age > mspan:
                self.__SeqIndex = 1
            else:
                self.__SeqIndex = 0
