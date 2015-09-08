from .orbitcontents import OrbitContent
from .satellites import Moon, Moonlet
from .tables import GGSizeTable

class GasGiant(OrbitContent):
    def __init__(self, primary, orbitalradius, rollbonus=True):
        OrbitContent.__init__(self, primary, orbitalradius)
        self.makesize(rollbonus)
        self.makemass()
        self.makediameter()
        self.makecloudtopgrav()
        self.makemoons()
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

    def get_size(self):
        return self.__size

    def printinfo(self):
        print("---- Gas Giant {} Properties ----".format(self.getName()))
        print("     Size:\t{}".format(self.__size))
        print("  BB Temp:\t{}".format(self.getBBTemp()))
        print("     Mass:\t{}".format(self.__mass))
        print("     Dens:\t{}".format(self.__density))
        print("     Diam:\t{}".format(self.__diameter))
        print("  Orb Per:\t{}".format(self.getPeriod()))
        print("  Orb Ecc:\t{}".format(self.getEcc()))
        print(" Cl Top G:\t{}".format(self.__gravity))
        print("  # 1st M:\t{}".format(len(self.__firstfamily)))
        print("  # 2nd M:\t{}".format(len(self.__secondfamily)))
        print("  # 3rd M:\t{}".format(len(self.__thirdfamily)))
        for moon in self.__secondfamily:
            moon.printinfo()
        print("------------------------------\n")

    def type(self):
        return "Gas Giant"

    def makemoons(self):
        self.makefirstfamily()
        self.makesecondfamily()
        self.makethirdfamily()

    def makefirstfamily(self):
        orbit = self.getOrbit()
        modifier = 0
        if orbit <= 0.1:
            modifier = -10
        if orbit > 0.1 and orbit <= 0.5:
            modifier = -8
        if orbit > 0.5 and orbit <= 0.75:
            modifier = -6
        if orbit > 0.75 and orbit <= 1.5:
            modifier = -3
        nummoonlets = self.roll(2, modifier)
        if nummoonlets < 0:
            nummoonlets = 0
        self.__firstfamily = [Moonlet(self, 'first') for nummoonlet in range(nummoonlets)]

    def makesecondfamily(self):
        orbit = self.getOrbit()
        modifier = 0
        if orbit <= 0.1:
            modifier = -200 # Equivalent to "do not roll"
        if orbit > 0.1 and orbit <= 0.5:
            modifier = -5
        if orbit > 0.5 and orbit <= 0.75:
            modifier = -3
        if orbit > 0.75 and orbit <= 1.5:
            modifier = -1
        nummoons = self.roll(1, modifier)
        if nummoons < 0:
            nummoons = 0
        self.__secondfamily = sorted([Moon(self, self.primarystar) for nummoon in range(nummoons)], key = lambda moon: moon.getOrbit())

    def makethirdfamily(self):
        orbit = self.getOrbit()
        modifier = 0
        if orbit <= 0.5:
            modifier = -200 # Equivalent to "do not roll"
        if orbit > 0.5 and orbit <= 0.75:
            modifier = -5
        if orbit > 0.75 and orbit <= 1.5:
            modifier = -4
        if orbit > 1.5 and orbit <= 3:
            modifier = -1
        nummoonlets = self.roll(1, modifier)
        if nummoonlets < 0:
            nummoonlets = 0
        self.__thirdfamily = [Moonlet(self, 'third') for nummoonlet in range(nummoonlets)]

    def makemass(self):
        size = self.get_size()
        diceroll = self.roll(3, 0)
        mass, density = GGSizeTable[size][diceroll]
        self.__mass = mass
        self.__density = density

    def getMass(self):
        return self.__mass

    def makediameter(self):
        self.__diameter = (self.__mass / self.__density) ** (1/3.)

    def getDiameter(self):
        return self.__diameter

    def makecloudtopgrav(self):
        self.__gravity = self.__density * self.__diameter

    def numMoons(self):
        return len(self.__secondfamily)

    def numMoonlets(self):
        return len(self.__firstfamily) + len(self.__thirdfamily)

    def setNumber(self, number):
        OrbitContent.setNumber(self, number)
        # Name the moons
        counter = 0
        for moon in self.__secondfamily:
            counter += 1
            moon.setNumber(counter)
            letter = self.primarystar.getLetter()
            name = '<{}-{}-{}>'.format(letter, number, counter)
            moon.setName(name)

    def getMoons(self):
        return self.__secondfamily

    def getDensity(self):
        return self.__density

    def getGravity(self):
        return self.__gravity

    def getFirstFamily(self):
        return self.__firstfamily

    def getThirdFamily(self):
        return self.__thirdfamily
