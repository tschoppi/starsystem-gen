import GURPS_Star as GS
import GURPS_Dice as GD

class StarSystem:
    roller = GD.DiceRoller()

    def __init__(self):
        self.__opencluster = self.randomcluster()
        self.__numstars = self.randomstars()
        self.makeage()
        self.printinfo()
        self.stars = []
        for i in range(self.__numstars):
            self.stars.append(GS.Star(age=self.__age))

    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def printinfo(self):
        print("Star System Info")
        print("================")
        print("        Age:\t{}".format(self.__age))
        print(" # of Stars:\t{}".format(self.__numstars))
        print("OpenCluster:\t{}".format(self.__opencluster))
        print("================\n")

    def randomcluster(self):
        # Criteria for a success (star system in an open cluster):
        #    - Roll of 10 or less
        return self.roll(3,0) <= 10

    def randomstars(self):
        if self.__opencluster:
            rollmod = 3
        else:
            rollmod = 0
        diceroll = self.roll(3,rollmod)

        if diceroll >= 16:
            return 3
        elif diceroll <= 10:
            return 1
        else:
            return 2

    def makeage(self):
        provage = self.randomage()
        while self.__opencluster and provage > 2:
            provage = self.randomage()
        self.__age = provage

    def randomage(self):
        diceroll = self.roll(3,0)
        if diceroll == 3:
            return 0
        elif diceroll <= 6:
            return 0.1 + self.roll(1,-1) * 0.3 + self.roll(1,-1) * 0.05
        elif diceroll <= 10:
            return 2.0 + self.roll(1,-1) * 0.6 + self.roll(1,-1) * 0.1
        elif diceroll <= 14:
            return 5.6 + self.roll(1,-1) * 0.6 + self.roll(1,-1) * 0.1
        elif diceroll <= 17:
            return 8.0 + self.roll(1,-1) * 0.6 + self.roll(1,-1) * 0.1
        else:
            return 10 + self.roll(1,-1) * 0.6 + self.roll(1,-1) * 0.1
