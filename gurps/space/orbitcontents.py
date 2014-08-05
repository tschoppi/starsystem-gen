# Here live all the GURPS Orbit Contents; Planets and Asteroid Belts, Moons and
# Moonlets
from . import dice as GD
from .tables import SizeToInt, IntToSize, MAtmoTable, TempFactor, WorldClimate
from .tables import SizeConstrTable, PressureCategory, GGSizeTable
from math import floor

class OrbitContent:
    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self,
                 primary,    # Primary star
                 orbitalradius):
        self.roller = GD.DiceRoller()
        self.__orbit = orbitalradius
        self.primarystar = primary
        primarylum = self.primarystar.getLuminosity()
        self.makebbtemp(primarylum, self.__orbit)

    def makebbtemp(self, lum, orb):
        self.__bbtemp = 278 * lum**(0.25) * orb**(-0.5)

    def getBBTemp(self):
        return self.__bbtemp

    def getOrbit(self):
        return self.__orbit




class World(OrbitContent):
    def __init__(self, primary, orbitalradius, sizeclass):
        OrbitContent.__init__(self, primary, orbitalradius)
        self.__sizeclass = sizeclass
        self.maketype()
        self.makeatmosphere()
        self.makehydrographics()
        self.makeclimate()
        self.makedensity()
        self.makediameter()
        self.makegravity()
        self.makemass()
        self.makepressure()

    def __repr__(self):
        return repr("World")

    def type(self):
        return "World"

    def getSize(self):
        return self.__sizeclass

    def maketype(self):
        bbtemp = self.getBBTemp()
        size = self.getSize()
        primmass = self.primarystar.getMass()
        type = 'Ice'
        if size == 'Tiny' and bbtemp >= 141:
            type = 'Rock'
        if size == 'Small':
            if bbtemp <= 80:
                type = 'Hadean'
            if bbtemp >= 141:
                type = 'Rock'
        if size == 'Standard':
            if bbtemp <= 80:
                type = 'Hadean'
        if size == 'Standard' or size == 'Large':
            if bbtemp > 150 and bbtemp <= 230 and primmass <= 0.65:
                type = 'Ammonia'
            if bbtemp > 240 and bbtemp <= 320:
                age = self.primarystar.getAge()
                if size == 'Standard':
                    cap = 10
                if size == 'Large':
                    cap = 5
                bonus = floor(age / 0.5)
                if bonus > cap:
                    bonus = cap
                dice = self.roll(3, bonus)
                if dice >= 18:
                    type = 'Garden'
                else:
                    type = 'Ocean'
            if bbtemp > 320 and bbtemp <= 500:
                type = 'Greenhouse'
            if bbtemp > 500:
                type = 'Chthonian'
        self.__type = type

    def getType(self):
        return self.__type

    def getAtmass(self):
        return self.__atmmass

    def makeatmosphere(self):
        size = self.getSize()
        type = self.getType()
        # Determine atmospheric mass
        if size == 'Tiny' or type == 'Hadean' or type == 'Chthonian' or  type == 'Rock':
            self.__atmmass = 0
        else:
            self.__atmmass = self.roll(3,0) / 10.

        # Now determine atmospheric composition
        self.atmcomp = {
            'Corrosive': False,
            'Mildly Toxic': False,
            'Highly Toxic': False,
            'Lethally Toxic': False,
            'Suffocating': False
        }
        self.__hasmarginal = False
        self.__marginal = ''
        if size == 'Small' and type == 'Ice':
            self.atmcomp['Suffocating'] = True
            if self.roll(3,0) > 15:
                self.atmcomp['Lethally Toxic'] = True
            else:
                self.atmcomp['Mildly Toxic'] = True

        if type == 'Ammonia' or type == 'Greenhouse':
            self.atmcomp['Suffocating'] = True
            self.atmcomp['Lethally Toxic'] = True
            self.atmcomp['Corrosive'] = True

        if type == 'Garden':
            if self.roll(3,0) >= 12:
                self.__hasmarginal = True
                self.__marginal = MAtmoTable[self.roll(3,0)]

        if size == 'Standard' and (type == 'Ice' or type == 'Ocean'):
            self.atmcomp['Suffocating'] = True
            if self.roll(3,0) > 12:
                self.atmcomp['Mildly Toxic'] = True

        if size == 'Large' and (type == 'Ice' or type == 'Ocean'):
            self.atmcomp['Highly Toxic'] = True
            self.atmcomp['Suffocating'] = True

    def getMarginal(self):
        """Return a tuple:
        (boolean: marginal, marginal atmosphere)
        """
        return (self.__hasmarginal, self.__marginal)

    def makehydrographics(self):
        hydro = 0
        size = self.getSize()
        type = self.getType()
        if size == 'Small' and type == 'Ice':
            hydro = self.roll(1,2) * 10
        if type == 'Ammonia':
            hydro = self.roll(2,0) * 10
            if hydro > 100:
                hydro = 100
        if type == 'Ice' and (size == 'Standard' or size == 'Large'):
            hydro = self.roll(2,-10) * 10
            if hydro < 0:
                hydro = 0
        if type == 'Ocean' or type == 'Garden':
            bonus = 4
            if size == 'Large':
                bonus = 6
            hydro = self.roll(1, bonus) * 10
            if hydro > 100:
                hydro = 100
        if type == 'Greenhouse':
            hydro = self.roll(2, -7) * 10
            if hydro < 0:
                hydro = 0
        self.__hydrocover = hydro

    def getHydrocover(self):
        return self.__hydrocover

    def absorptiongreenhouse(self):
        """
        Return a tuple (absorption factor, greenhouse factor) based on world
        type and size.
        """
        type = self.getType()
        size = self.getSize()
        if type is not 'Garden' and type is not 'Ocean':
            return TempFactor[type][size]
        else:
            hydro = self.getHydrocover()
            abs = 0.84
            if hydro <= 90:
                abs = 0.88
            if hydro <= 50:
                abs = 0.92
            if hydro <= 20:
                abs = 0.95
            return (abs, 0.16)

    def makeclimate(self):
        abs, green = self.absorptiongreenhouse()
        matm  = self.getAtmass()
        bbcorr = abs * (1 + (matm * green))
        self.__averagesurface = bbcorr * self.getBBTemp()
        self.__climatetype = WorldClimate(self.__averagesurface)

    def getAvSurf(self):
        return self.__averagesurface

    def getClimate(self):
        return self.__climatetype

    def makedensity(self):
        type = self.getType()
        size = self.getSize()
        density = 0
        dice = self.roll(3,0)
        if type == 'Ammonia' or type == 'Hadean' or type == 'Sulfur' or (type == 'Ice' and size != 'Large'):
            if dice >= 3:
                density = 0.3
            if dice >= 7:
                density = 0.4
            if dice >= 11:
                density = 0.5
            if dice >= 15:
                density = 0.6
            if dice == 18:
                density = 0.7
        elif type == 'Rock':
            if dice >= 3:
                density = 0.6
            if dice >= 7:
                density = 0.7
            if dice >= 11:
                density = 0.8
            if dice >= 15:
                density = 0.9
            if dice == 18:
                density = 1.0
        else:
            if dice >= 3:
                density = 0.8
            if dice >= 7:
                density = 0.9
            if dice >= 11:
                density = 1.0
            if dice >= 15:
                density = 1.1
            if dice == 18:
                density = 1.2
        self.__density = density

    def getDensity(self):
        return self.__density

    def makediameter(self):
        size = self.getSize()
        bb = self.getBBTemp()
        dens = self.getDensity()
        smin, smax = SizeConstrTable[size]
        term = (bb / dens) ** (0.5)
        min = term * smin
        max = term * smax
        diff = max - min
        diam = self.roll(2, -2) * 0.1 * diff + min
        self.__diameter = diam

    def getDiameter(self):
        return self.__diameter

    def makegravity(self):
        self.__surfacegravity = self.getDensity() * self.getDiameter()

    def getGravity(self):
        return self.__surfacegravity

    def makemass(self):
        self.__mass = self.getDensity() * self.getDiameter() ** 3

    def getMass(self):
        return self.__mass

    def makepressure(self):
        size = self.getSize()
        type = self.getType()
        pressure = 0
        if size == 'Tiny' or type == 'Hadean':
            category = 'None'
        elif type == 'Chthonian':
            category = 'Trace'
        elif size == 'Small' and type == 'Rock':
            category = 'Trace'
        else:
            factor = 1
            if size == 'Small' and type == 'Ice':
                factor = 10
            if size == 'Large':
                factor = 5
            if type == 'Greenhouse':
                factor *= 100
            pressure = self.getMass() * factor * self.getGravity()
            category = PressureCategory(pressure)
        self.__pressure = pressure
        self.__presscat = category

    def getPressure(self):
        return self.__pressure

    def getPressCat(self):
        return self.__presscat

    def makevolcanism(self):
        bonus = self.getGravity() / self.primarystar.getAge()
        bonus += self.volcanicbonus()
        volcanoroll = self.roll(3, bonus)
        activity = 'None'
        if volcanoroll > 16:
            activity = 'Light'
        if volcanoroll > 20:
            activity = 'Moderate'
        if volcanoroll > 26:
            activity = 'Heavy'
        if volcanoroll > 70:
            activity = 'Extreme'
        self.__volcanism = activity

    def getVolcanism(self):
        return self.__volcanism

    def volcanicbonus(self):
        return 0

    def maketectonism(self):
        if self.getSize() == 'Small' or self.getSize() == 'Tiny':
            self.__tectonic = 'None'
        else:
            volc = self.getVolcanism()
            bonus = 0
            if volc == 'None':
                bonus -= 8
            if volc == 'Light':
                bonus -= 4
            if volc == 'Heavy':
                bonus += 4
            if volc == 'Extreme':
                bonus += 8
            if self.getHydrocover() < 50:
                bonus -= 2
            bonus += self.tectonicbonus()
            tect = self.roll(3, bonus)
            activity = 'None'
            if tect > 6:
                activity = 'Light'
            if tect > 10:
                activity = 'Moderate'
            if tect > 14:
                activity = 'Heavy'
            if tect > 18:
                activity = 'Extreme'
            self.__tectonic = activity

    def tectonicbonus(self):
        return 0

    def getTectonics(self):
        return self.__tectonic

    def resourcebonus(self):
        volc = self.getVolcanism()
        bonus = 0
        if volc == 'None':
            bonus -= 2
        if volc == 'Light':
            bonus -= 1
        if volc == 'Heavy':
            bonus += 1
        if volc == 'Extreme':
            bonus += 2
        return bonus

    def makeresources(self):
        rollbonus = self.resourcebonus()
        dice = self.roll(3, rollbonus)
        rvm = -3
        value = 'Scant'
        if dice > 2:
            rvm = -2
            value = 'Very Poor'
        if dice > 4:
            rvm = -1
            value = 'Poor'
        if dice > 7:
            rvm = 0
            value = 'Average'
        if dice > 13:
            rvm = 1
            value = 'Abundant'
        if dice > 16:
            rvm = 2
            value = 'Very Abundant'
        if dice> 18:
            rvm = 3
            value = 'Rich'
        self.__rvm = rvm
        self.__resources = value

    def getRVM(self):
        return self.__rvm

    def getResources(self):
        return self.__resources




class Planet(World):
    def __init__(self, primary, orbitalradius, sizeclass):
        World.__init__(self, primary, orbitalradius, sizeclass)
        self.generatemoons()
        self.makevolcanism()
        self.maketectonism()
        self.makeresources()

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
        print("       Res. V:\t{}\n".format(self.getResources()))
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


class AsteroidBelt(OrbitContent):
    def __init__(self, primarystar, orbitalradius):
        OrbitContent.__init__(self, primarystar, orbitalradius)
        self.makeresources()

    def __repr__(self):
        return repr("Asteroid Belt")

    def type(self):
        return "Asteroid Belt"

    def printinfo(self):
        print("Asteroid Belt")
        print("    Orbit:\t{}".format(self.getOrbit()))
        print("      RVM:\t{}".format(self.__rvm))
        print("   Res. V:\t{}\n".format(self.__resources))

    def makeresources(self):
        dice = self.roll(3,0)
        rvm = -5
        value = 'Worthless'
        if dice == 4:
            rvm = -4
            value = 'Very Scant'
        if dice == 5:
            rvm = -3
            value = 'Scant'
        if dice >= 6 and dice <= 7:
            rvm = -2
            value = 'Very Poor'
        if dice >= 8 and dice <= 9:
            rvm = -1
            value = 'Poor'
        if dice >= 10 and dice <= 11:
            rvm = 0
            value = 'Average'
        if dice >= 12 and dice <= 13:
            rvm = 1
            value = 'Abundant'
        if dice >= 14 and dice <= 15:
            rvm = 2
            value = 'Very Abundant'
        if dice == 16:
            rvm = 3
            value = 'Rich'
        if dice == 17:
            rvm = 4
            value = 'Very Rich'
        if dice == 16:
            rvm = 5
            value = 'Motherlode'
        self.__rvm = rvm
        self.__resources = value




class GasGiant(OrbitContent):
    def __init__(self, primary, orbitalradius, rollbonus=True):
        OrbitContent.__init__(self, primary, orbitalradius)
        self.makesize(rollbonus)
        self.makemoons()
        self.makemass()
        self.makediameter()
        self.makecloudtopgrav()
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

    def getSize(self):
        return self.__size

    def printinfo(self):
        print("---- Gas Giant Properties ----")
        print("     Size:\t{}".format(self.__size))
        print("  BB Temp:\t{}".format(self.getBBTemp()))
        print("     Mass:\t{}".format(self.__mass))
        print("     Dens:\t{}".format(self.__density))
        print("     Diam:\t{}".format(self.__diameter))
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
        self.__firstfamily = [Moonlet(self) for nummoonlet in range(nummoonlets)]

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
        self.__secondfamily = [Moon(self, self.primarystar) for nummoon in range(nummoons)]

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
        self.__thirdfamily = [Moonlet(self) for nummoonlet in range(nummoonlets)]

    def makemass(self):
        size = self.getSize()
        diceroll = self.roll(3, 0)
        mass, density = GGSizeTable[size][diceroll]
        self.__mass = mass
        self.__density = density

    def makediameter(self):
        self.__diameter = (self.__mass / self.__density) ** (1/3.)

    def makecloudtopgrav(self):
        self.__gravity = self.__density * self.__diameter




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

    def printinfo(self):
        print("         *** Moon Information *** ")
        #print("Parent Planet:\t{}".format(self.parent))
        print("           World Type:\t{} ({})".format(self.__sizeclass, self.getType()))
        print("                Orbit:\t{}".format(self.__orbit))
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
        print("               Res. V:\t{}\n".format(self.getResources()))
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


class Moonlet:
    def roll(self, ndice, modifier):
        return self.roller.roll(ndice, modifier)

    def __init__(self, parentplanet):
        self.parent = parentplanet
        self.roller = GD.DiceRoller()

    def printinfo(self):
        print("Moonlet Information")
        print("Parent Planet:\t{}".format(self.parent))
