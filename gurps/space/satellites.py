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

    def printinfo(self):
        print("         *** Moon Information *** ")
        #print("Parent Planet:\t{}".format(self.parent))
        print("           World Type:\t{} ({})".format(self.__sizeclass, self.getType()))
        print("                Orbit:\t{} Earth Diameters".format(self.__orbit))
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



class Moonlet:
    def roll(self, ndice, modifier):
        return self.roller.roll(ndice, modifier)

    def __init__(self, parentplanet):
        self.parent = parentplanet
        self.roller = GD.DiceRoller()

    def printinfo(self):
        print("Moonlet Information")
        print("Parent Planet:\t{}".format(self.parent))
