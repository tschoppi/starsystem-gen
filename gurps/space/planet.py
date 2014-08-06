from .world import World
from .satellites import Moon, Moonlet
from .tables import SizeToInt

class Planet(World):
    def __init__(self, primary, orbitalradius, sizeclass):
        World.__init__(self, primary, orbitalradius, sizeclass)
        self.generatemoons()
        self.makevolcanism()
        self.maketectonism()
        self.makeresources()
        self.makehabitability()
        self.makeaffinity()

    def printinfo(self):
        print("--- Planet Info ---")
        print("        Orbit:\t{}".format(self.getOrbit()))
        print("   World Type:\t{} ({})".format(self.getSize(), self.getType()))
        if self.__nummoons > 0:
            print("      # Moons:\t{}".format(self.__nummoons))
            for moon in self.__moons:
                moon.printinfo()
        if self.__nummoonlets > 0:
            print("    # Moonlts:\t{}".format(self.__nummoonlets))
        self.printatmosphere()
        print("  Hydrogr Cov:\t{}".format(self.getHydrocover()))
        print("    Av Surf T:\t{}".format(self.getAvSurf()))
        print("      Climate:\t{}".format(self.getClimate()))
        print("      Density:\t{}".format(self.getDensity()))
        print("     Diameter:\t{}".format(self.getDiameter()))
        print("    Surf Grav:\t{}".format(self.getGravity()))
        print("         Mass:\t{}".format(self.getMass()))
        print("     Pressure:\t{} ({})".format(self.getPressure(), self.getPressCat()))
        print("    Volcanism:\t{}".format(self.getVolcanism()))
        print("    Tectonics:\t{}".format(self.getTectonics()))
        print("          RVM:\t{}".format(self.getRVM()))
        print("       Res. V:\t{}".format(self.getResources()))
        print(" Habitability:\t{}".format(self.getHabitability()))
        print("     Affinity:\t{}".format(self.getAffinity()))
        print("     Orb Per.:\t{}".format(self.getPeriod()))
        print("------------------- \n")

    def printatmosphere(self):
        atcomp = self.atmcomp
        bmarg, marg = self.getMarginal()
        atmcomp = [key for key in atcomp.keys() if atcomp[key] == True]
        if len(atmcomp) > 0:
            print("     Atm Comp:\t{}".format(atmcomp))
        if bmarg:
            print("     Marginal:\t{}".format(marg))

    def __repr__(self):
        return repr("{} Terrestrial Planet".format(self.getSize()))

    def type(self):
        return "Terrestrial World"

    def generatemoons(self):
        rollmod = -4
        rollmod += self.moonrollmodifier()
        moonroll = self.roll(1, rollmod)
        if moonroll <= 0:
            moonroll = 0
            # If we have no major moons, generate moonlets
            self.generatemoonlets()
        else:
            self.__nummoonlets = 0
            self.__moonlets = []
        self.__nummoons = moonroll
        self.__moons = [Moon(self, self.primarystar) for moonnum in range(moonroll)]

    def generatemoonlets(self):
        rollmod = -2
        rollmod += self.moonrollmodifier()
        moonletroll = self.roll(1, rollmod)
        if moonletroll < 0:
            moonletroll = 0
        self.__nummoonlets = moonletroll
        self.__moonlets = [Moonlet(self) for moonletnum in range(moonletroll)]

    def moonrollmodifier(self):
        modifier = 0
        orbit = self.getOrbit()
        if orbit <= 0.5:
            return -20 # Equivalent to "do not roll"
        if orbit > 0.5 and orbit <= 0.75:
            modifier -= 3
        if orbit > 0.75 and orbit <= 1.5:
            modifier -= 1
        modifier += (SizeToInt[self.getSize()] - 2)
        return modifier

    def getSatellites(self):
        if self.__nummoons > 0:
            return self.__moons
        if self.__nummoonlets > 0:
            return self.__moonlets

    def volcanicbonus(self):
        if self.__nummoons == 1:
            return 5
        if self.__nummoons > 1:
            return 10
        return 0

    def tectonicbonus(self):
        if self.__nummoons == 1:
            return 2
        if self.__nummoons > 1:
            return 4
        return 0
