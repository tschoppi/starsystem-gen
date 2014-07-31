from . import star as GS
from . import dice as GD
from .tables import OrbSepTable, StOEccTable

class StarSystem:
    roller = GD.DiceRoller()

    def __init__(self, **kwargs):
        opencluster = kwargs.get('opencluster', None)
        if opencluster is not None:
            self.__opencluster = opencluster
        else:
            self.__opencluster = self.randomcluster()

        numstars = kwargs.get('numstars', None)
        if numstars is not None:
            if numstars > 0 and numstars <= 3:
                self.__numstars = numstars
            else:
                self.__numstars = self.randomstarnum()
        else:
            self.__numstars = self.randomstarnum()

        age = kwargs.get('age', None)
        self.makeage(age)
        self.generatestars()
        self.sortstars()
        self.makeorbits()
        self.makeminmaxseps()
        self.makeforbiddenzones()
        self.createplanetsystem()
        self.printinfo()

    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def printinfo(self):
        print("Star System Info")
        print("================")
        print("        Age:\t{}".format(self.__age))
        print(" # of Stars:\t{}".format(self.__numstars))
        print("OpenCluster:\t{}".format(self.__opencluster))
        print("Stellar Orb:\t{}".format(self.__orbits))
        print("StOrbMinMax:\t{}".format(self.__minmaxorbits))
        print("================\n")
        for i in range(self.__numstars):
            self.stars[i].printinfo()

    def randomcluster(self):
        # Criteria for a success (star system in an open cluster):
        #    - Roll of 10 or less
        return self.roll(3,0) <= 10

    def randomstarnum(self):
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

    def generatestars(self):
        self.stars = []
        for i in range(self.__numstars):
            self.stars.append(GS.Star(age=self.__age))

    def makeage(self, age):
        if age is None:
            provage = self.randomage()
            while self.__opencluster and provage > 2:
                provage = self.randomage()
            self.__age = provage
        else:
            self.__age = age

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

    # Sort the stars according to mass. Higher mass is placed first.
    def sortstars(self):
        num = self.__numstars
        newlist = []
        for i in range(num):
            highest = 0    # Index of the star with the highest mass, reset to 0
            for j in range(len(self.stars)):
                if self.stars[highest].getMass() < self.stars[j].getMass():
                    highest = j
            newlist.append(self.stars[highest])
            del self.stars[highest]

        self.stars = newlist

    # Generate stellar orbits for multiple-star systems
    # Missing: Sub-companion star for distant second companion star
    # Missing: Ensuring that the orbital separation of the second companion is
    #          larger than the separation of the first
    def makeorbits(self):
        self.__orbsepentry = []
        self.__orbits = []
        if self.__numstars == 1:
            # Don't do anything for just one star
            return None
        if self.__numstars >= 2:
            dice = self.roll(3,0)
            osepindex = self.findorbsepindex(dice)
            orbsep = OrbSepTable[osepindex]
            orbit = self.roll(2,0) * orbsep[1]

            eccmod = orbsep[2]
            eccroll = self.roll(3,eccmod)
            if eccroll < 3:
                eccroll = 3
            if eccroll > 18:
                eccroll = 18
            eccentricity = StOEccTable[eccroll]

            self.__orbsepentry.append(orbsep)
            self.__orbits.append((orbit, eccentricity))
        if self.__numstars == 3:
            dice = self.roll(3,6)
            osepindex = self.findorbsepindex(dice)
            orbsep = OrbSepTable[osepindex]
            orbit = self.roll(2,0) * orbsep[1]

            eccmod = orbsep[2]
            eccroll = self.roll(3,eccmod)
            if eccroll < 3:
                eccroll = 3
            if eccroll > 18:
                eccroll = 18
            eccentricity = StOEccTable[eccroll]

            self.__orbsepentry.append(orbsep)
            self.__orbits.append((orbit, eccentricity))

            # Recursively contine until second companion is significantly
            # further away than the first
            if self.__orbsepentry[0][1] >= self.__orbsepentry[1][1]:
                return self.makeorbits()



    def findorbsepindex(self, diceroll):
        if diceroll <= 6:
            return 0
        if diceroll <= 9:
            return 1
        if diceroll <= 11:
            return 2
        if diceroll <= 14:
            return 3
        else:
            return 4

    def makeminmaxseps(self):
        self.__minmaxorbits = []
        for i in range(len(self.__orbits)):
            orbit, ecc = self.__orbits[i]
            min = (1 - ecc) * orbit
            max = (1 + ecc) * orbit
            self.__minmaxorbits.append((min, max))

    def makeforbiddenzones(self):
        self.__forbiddenzones = []
        for i in range(len(self.__minmaxorbits)):
            min, max = self.__minmaxorbits[i]
            start = min / 3.
            end = max * 3.
            self.__forbiddenzones.append((start, end))

            # Tell the stars their forbidden zones
            if i == 0: # For the first two stars
                self.stars[0].setForbiddenZone(start, end)
                self.stars[1].setForbiddenZone(start, end)
            if i == 1: # For the third star
                self.stars[2].setForbiddenZone(start, end)

    def createplanetsystem(self):
        for star in self.stars:
            star.makeplanetsystem()
