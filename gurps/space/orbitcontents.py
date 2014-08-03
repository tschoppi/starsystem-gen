# Here live all the GURPS Orbit Contents; Planets and Asteroid Belts, Moons and
# Moonlets
from . import dice as GD
from .tables import SizeToInt, IntToSize, MAtmoTable
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



class Planet(World):
    def __init__(self, primary, orbitalradius, sizeclass):
        World.__init__(self, primary, orbitalradius, sizeclass)
        self.generatemoons()

    def printinfo(self):
        print("Planet Info")
        print("        Orbit:\t{}".format(self.getOrbit()))
        print("   World Type:\t{} ({})".format(self.getSize(), self.getType()))
    #    print("         Type:\t{}".format(self.getType()))
        print("      # Moons:\t{}".format(self.__nummoons))
        print("    # Moonlts:\t{}".format(self.__nummoonlets))
        self.printatmosphere()
        print("  Hydrogr Cov:\t{}".format(self.getHydrocover()))

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



class AsteroidBelt(OrbitContent):
    def __repr__(self):
        return repr("Asteroid Belt")

    def type(self):
        return "Asteroid Belt"

    def printinfo(self):
        print("Asteroid Belt")
        print("    Orbit:\t{}".format(self.getOrbit()))




class GasGiant(OrbitContent):
    def __init__(self, primary, orbitalradius, rollbonus=True):
        OrbitContent.__init__(self, primary, orbitalradius)
        self.makesize(rollbonus)
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

    def getSize(self):
        return self.__size

    def printinfo(self):
        print("Gas Giant Properties")
        print("     Size:\t{}".format(self.__size))
        print("  BB Temp:\t{}".format(self.getBBTemp()))
        print("  # 1st M:\t{}".format(len(self.__firstfamily)))
        print("  # 2nd M:\t{}".format(len(self.__secondfamily)))
        print("  # 3rd M:\t{}".format(len(self.__thirdfamily)))

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

    def printinfo(self):
        print("Moon Information")
        print("Parent Planet:\t{}".format(self.parent))
        print("   Size Class:\t{}".format(self.__sizeclass))
        print("        Orbit:\t{}".format(self.__orbit))

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



class Moonlet:
    def roll(self, ndice, modifier):
        return self.roller.roll(ndice, modifier)

    def __init__(self, parentplanet):
        self.parent = parentplanet
        self.roller = GD.DiceRoller()

    def printinfo(self):
        print("Moonlet Information")
        print("Parent Planet:\t{}".format(self.parent))
