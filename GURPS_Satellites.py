# Here live all the GURPS satellites: Moons and Moonlets
import GURPS_Dice as GD
from GURPS_Tables import SizeToInt, IntToSize

class Satellite:
    def roll(self, ndice, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self, parentplanet):
        self.parent = parentplanet
        self.roller = GD.DiceRoller()

class Moon(Satellite):
    def __init__(self, parentplanet):
        Satellite.__init__(self, parentplanet)
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

class Moonlet(Satellite):
    def printinfo(self):
        print("Moonlet Information")
        print("Parent Planet:\t{}".format(self.parent))
