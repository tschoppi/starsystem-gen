from . import dice as GD
from .world import World
from .tables import SizeToInt, IntToSize

class Moon(World):
    def __init__(self, parentplanet, primarystar):
        self.roller = GD.DiceRoller()
        self.parent = parentplanet
        self.primarystar = primarystar
        self.makebbtemp()
        self.__orbit = None
        self.makesize()
        self.maketype()
        self.makeatmosphere()
        self.makehydrographics()
        self.makeclimate()
        self.makedensity()
        self.makediameter()
        self.makegravity()
        self.makemass()
        self.makepressure()
        self.makevolcanism()
        self.maketectonism()
        self.makeresources()
        self.makehabitability()
        self.makeaffinity()
        self.makeorbit()
        self.makeperiod()
        self.maketidals()
        self.makerotation()
        self.makecalendar()

    def printinfo(self):
        print("         *** Moon Information *** ")
        #print("Parent Planet:\t{}".format(self.parent))
        print("           World Type:\t{} ({})".format(self.__sizeclass, self.getType()))
        print("                Orbit:\t{} Earth Diameters".format(self.__orbit))
        print("             Orb Per.:\t{} d".format(self.getPeriod()))
        print("             Rot Per.:\t{} d".format(self.getRotation()))
        print("           Len of day:\t{} d".format(self.getDayLength()))
        print("         Len of Plday:\t{} d".format(self.getPlanetLength()))
        print("          Hydrogr Cov:\t{}".format(self.getHydrocover()))
        print("            Av Surf T:\t{}".format(self.getAvSurf()))
        print("              Climate:\t{}".format(self.getClimate()))
        print("              Density:\t{}".format(self.getDensity()))
        print("             Diameter:\t{}".format(self.getDiameter()))
        print("            Surf Grav:\t{}".format(self.getGravity()))
        print("                 Mass:\t{}".format(self.getMass()))
        print("             Pressure:\t{} ({})".format(self.getPressure(), self.getPressCat()))
        print("            Volcanism:\t{}".format(self.getVolcanism()))
        print("            Tectonics:\t{}".format(self.getTectonics()))
        print("                  RVM:\t{}".format(self.getRVM()))
        print("               Res. V:\t{}".format(self.getResources()))
        print("         Habitability:\t{}".format(self.getHabitability()))
        print("             Affinity:\t{}".format(self.getAffinity()))
        print("                  TTE:\t{}".format(self.getTTE()))
        print("         --- **************** --- \n")

    def makebbtemp(self):
        self.__bbtemp = self.parent.getBBTemp()
    def getBBTemp(self):
        return self.__bbtemp

    def makesize(self):
        parent = self.parent
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

    def getSize(self):
        return self.__sizeclass

    def setOrbit(self, orbit):
        self.__orbit = orbit

    def roll(self, ndice, modifier):
        return self.roller.roll(ndice, modifier)

    def volcanicbonus(self):
        if self.getType() == 'Sulfur':
            return 60
        if self.parent.type() == "Gas Giant":
            return 5
        return 0

    def makeorbit(self):
        """
        Randomly generate the orbit of this satellite, distinguishing between
        parent planets that are terrestrial or gas giants.
        """
        ptype = self.parent.type()
        if ptype == 'Terrestrial World':
            # Check for size difference and infer roll bonus from it
            psize = SizeToInt[self.parent.getSize()]
            osize = SizeToInt[self.getSize()]
            diff = psize - osize
            bonus = 0
            if diff == 2:
                bonus = 2
            if diff == 1:
                bonus = 4
            dice = self.roll(2, bonus)
            self.__orbit = dice * 2.5 * self.parent.getDiameter()
        if ptype == 'Gas Giant':
            roll = self.roll(3, 3)
            if roll >= 15:
                roll += self.roll(2, 0)
            self.__orbit = roll / 2. * self.parent.getDiameter()

    def getOrbit(self):
        return self.__orbit

    def makeperiod(self):
        m1 = self.getMass()
        mp = self.parent.getMass()
        m = m1 + mp
        orbit = self.getOrbit()
        self.__period = 0.166 * (orbit**3 / m)**(0.5)

    def getPeriod(self):
        return self.__period

    def maketidals(self):
        m = self.parent.getMass()
        d = self.getDiameter()
        r = self.getOrbit()
        tidal = 2230000 * m * d / r**3
        tte = tidal * self.primarystar.getAge() / m
        self.__tte = round(tte)

    def getTTE(self):
        return self.__tte

    def makerotation(self):
        if self.getTTE() > 50:
            rotperiod = self.getPeriod()  # [d]
        else:
            if self.getSize() == 'Large':
                bonus = 6
            if self.getSize() == 'Standard':
                bonus = 10
            if self.getSize() == 'Small':
                bonus = 14
            if self.getSize() == 'Tiny':
                bonus = 18
            diceroll = self.roll(3, bonus)
            rotperiod = (diceroll + self.getTTE()) / 24.
            if rotperiod > 1.5 or diceroll - bonus >= 16:
                roll2 = self.roll(2, 0)
                if roll2 == 7:
                    rotperiod = self.roll(1, 0) * 2
                if roll2 == 8:
                    rotperiod = self.roll(1, 0) * 5
                if roll2 == 9:
                    rotperiod = self.roll(1, 0) * 10
                if roll2 == 10:
                    rotperiod = self.roll(1, 0) * 20
                if roll2 == 11:
                    rotperiod = self.roll(1, 0) * 50
                if roll2 == 12:
                    rotperiod = self.roll(1, 0) * 100
            if rotperiod > self.getPeriod():
                rotperiod = self.getPeriod()
        if self.roll(3, 0) >= 17:
            rotperiod = -rotperiod
        self.__rotperiod = rotperiod

    def getRotation(self):
        return self.__rotperiod

    def makecalendar(self):
        # Calculate apparent length of a day for this moon
        s = self.parent.getPeriod() * 365.26  # [d]
        r = self.getRotation()  # [d]
        if s == r:
            alen = None
        else:
            alen = s * r / (s - r)
        self.__alenday = alen

        # Calculate the time in which the planet can be seen
        s = self.getPeriod()  # [d]
        if s == r:
            alen = None
        else:
            alen = s * r / (s - r)
        self.__alenplanet = alen

    def getDayLength(self):
        return self.__alenday

    def getPlanetLength(self):
        return self.__alenplanet



class Moonlet:
    def roll(self, ndice, modifier):
        return self.roller.roll(ndice, modifier)

    def __init__(self, parentplanet, family=None):
        self.parent = parentplanet
        self.roller = GD.DiceRoller()
        self.family = family
        self.makeorbit()
        self.makeperiod()

    def printinfo(self):
        print("Moonlet Information")
        print("Parent Planet:\t{}".format(self.parent))
        print("        Orbit:\t{} Earth Diameters".format(self.getOrbit()))
        print("      Orb Per:\t{} d".format(self.getPeriod()))

    def makeorbit(self):
        ptype = self.parent.type()
        if ptype == 'Gas Giant' and self.family == 'first':
            self.__orbit = self.roll(1, 4) / 4. * self.parent.getDiameter()
        if ptype == 'Gas Giant' and self.family == 'third':
            # Make random orbits between 20 and 200 planetary diameters
            import random as r
            multiplier = r.uniform(20, 200)
            self.__orbit = multiplier * self.parent.getDiameter()

        if ptype == 'Terrestrial World':
            self.__orbit = self.roll(1, 4) / 4. * self.parent.getDiameter()

    def getOrbit(self):
        return self.__orbit

    def makeperiod(self):
        m = self.parent.getMass()
        orbit = self.getOrbit()
        self.__period = 0.166 * (orbit**3 / m)**(0.5)

    def getPeriod(self):
        return self.__period
