from .world import World
from .satellites import Moon, Moonlet
from .tables import SizeToInt

class Planet(World):
    def __init__(self, primary, orbitalradius, sizeclass):
        World.__init__(self, primary, orbitalradius, sizeclass)
        self.generatemoons()
        self.maketidals()
        self.makerotation()
        self.makevolcanism()
        self.maketectonism()
        self.makeresources()
        self.makehabitability()
        self.makeaffinity()
        self.makecalendar()
        self.makeaxialtilt()

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
        print("     Orb Ecc.:\t{}".format(self.getEcc()))
        print("          TTE:\t{}".format(self.getTTE()))
        print("     Rot Per.:\t{} d".format(self.getRotation()))
        print("      Day Len:\t{} d".format(self.getDayLength()))
        if self.getMoonLengths() is not None:
            print("     Moon Len:\t{} d".format(self.getMoonLengths()))
        print("      Ax Tilt:\t{}".format(self.getAxialTilt()))
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
        return "Terrestrial"

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
        self.__moons = sorted([Moon(self, self.primarystar) for moonnum in range(moonroll)], key = lambda moon: moon.getOrbit())

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

    def maketidals(self):
        # Collect tidal effects for Moons
        moontide = 0
        if self.__nummoons > 0:
            moons = self.getSatellites()
            for moon in moons:
                m = moon.getMass()
                r = moon.getOrbit()
                d = self.getDiameter()
                moontide += 2230000 * m * d / r**3
        # Make tidal effect for star
        sunmass = self.primarystar.getMass()
        diameter = self.getDiameter()
        orbit = self.getOrbit()
        startide = 0.46 * sunmass * diameter / orbit**3
        totaltide = (moontide + startide) * self.primarystar.getAge() / self.getMass()
        self.__tte = round(totaltide)

    def getTTE(self):
        return self.__tte

    def makerotation(self):
        if self.getTTE() > 50:
            if self.__nummoons == 0:
                rotperiod = self.getPeriod() * 365.26
            else:
                # Find innermost moon and its orbital period
                moons = sorted(self.getSatellites(), key = lambda moon: moon.getOrbit())
                innermoon = moons[0]
                rotperiod = innermoon.getPeriod()
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
            if rotperiod > self.getPeriod() * 365.26:
                rotperiod = self.getPeriod() * 365.26
        if self.roll(3, 0) >= 13:
            rotperiod = -rotperiod
        self.__rotperiod = rotperiod

    def getRotation(self):
        return self.__rotperiod

    def makecalendar(self):
        """Make the local calendar, including:

            - Apparent length of day
            - Apparent length of moon cycles
        """
        s = self.getPeriod() * 365.26
        r = self.getRotation()
        if s == r:
            alen = None
        else:
            alen = s * r / (s - r)
        self.__daylength = alen

        if self.__nummoons > 0:
            self.__moonlength = []
            for moon in self.getSatellites():
                s = moon.getPeriod()
                if s == r:
                    alen = None
                else:
                    alen = s * r / (s - r)
                self.__moonlength.append(alen)

    def getDayLength(self):
        return self.__daylength

    def getMoonLengths(self):
        if self.__nummoons > 0:
            return self.__moonlength
        else:
            return None

    def makeaxialtilt(self):
        roll1 = self.roll(3, 0)
        base = 0
        if roll1 > 6:
            base = 10
        if roll1 > 9:
            base = 20
        if roll1 > 12:
            base = 30
        if roll1 > 14:
            base = 40
        if roll1 > 16:
            roll2 = self.roll(1, 0)
            if roll2 in [1, 2]:
                base = 50
            if roll2 in [3, 4]:
                base = 60
            if roll2 == 5:
                base = 70
            if roll2 == 6:
                base = 80
        self.__axtilt = base + self.roll(2, -2)

    def getAxialTilt(self):
        return self.__axtilt

    def numMoons(self):
        return self.__nummoons

    def numMoonlets(self):
        return self.__nummoonlets
