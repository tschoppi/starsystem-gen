from . import dice as GD
from .world import World
from .tables import SizeToInt, IntToSize


class Moon(World):
    def __init__(self, parent_planet, primary_star):
        self.roller = GD.DiceRoller()
        self.parent = parent_planet
        self.primary_star = primary_star
        self.make_blackbody_temperature()
        self.__orbit = None
        self.make_size()
        self.make_type()
        self.makeatmosphere()
        self.make_hydrographics()
        self.make_climate()
        self.make_density()
        self.make_diameter()
        self.make_gravity()
        self.make_mass()
        self.make_pressure()
        self.make_volcanism()
        self.make_tectonism()
        self.make_resources()
        self.make_habitability()
        self.make_affinity()
        self.make_orbit()
        self.make_period()
        self.make_tidals()
        self.make_rotation()
        self.make_calendar()

    def print_info(self):
        print("         *** Moon {} Information *** ".format(self.get_name()))
        # print("Parent Planet:\t{}".format(self.parent))
        print("           World Type:\t{} ({})".format(self.__sizeclass, self.get_type()))
        print("                Orbit:\t{} Earth Diameters".format(self.__orbit))
        print("             Orb Per.:\t{} d".format(self.get_period()))
        print("             Rot Per.:\t{} d".format(self.get_rotation()))
        print("           Len of day:\t{} d".format(self.get_day_length()))
        print("         Len of Plday:\t{} d".format(self.get_planet_length()))
        print("          Hydrogr Cov:\t{}".format(self.get_hydrographic_cover()))
        print("            Av Surf T:\t{}".format(self.get_average_surface_temp()))
        print("              Climate:\t{}".format(self.get_climate()))
        print("              Density:\t{}".format(self.get_density()))
        print("             Diameter:\t{}".format(self.get_diameter()))
        print("            Surf Grav:\t{}".format(self.get_gravity()))
        print("                 Mass:\t{}".format(self.get_mass()))
        print("             Pressure:\t{} ({})".format(self.get_pressure(), self.get_pressure_category()))
        print("            Volcanism:\t{}".format(self.get_volcanism()))
        print("            Tectonics:\t{}".format(self.get_tectonics()))
        print("                  RVM:\t{}".format(self.get_rvm()))
        print("               Res. V:\t{}".format(self.get_resources()))
        print("         Habitability:\t{}".format(self.get_habitability()))
        print("             Affinity:\t{}".format(self.get_affinity()))
        print("                  TTE:\t{}".format(self.get_total_tidal_effect()))
        print("         --- **************** --- \n")

    def make_blackbody_temperature(self):
        self.__bbtemp = self.parent.get_blackbody_temp()

    def get_blackbody_temp(self):
        return self.__bbtemp

    def make_size(self):
        parent = self.parent
        parentsize = SizeToInt[parent.get_size()]
        if parent.type() == "Gas Giant":
            parentsize = SizeToInt["Large"]
        diceroll = self.roll(3, 0)
        if diceroll >= 15:
            childsize = parentsize - 1
        if diceroll >= 12:
            childsize = parentsize - 2
        else:
            childsize = parentsize - 3
        if childsize < 0:
            childsize = 0
        self.__sizeclass = IntToSize[childsize]

    def get_size(self):
        return self.__sizeclass

    def set_orbit(self, orbit):
        self.__orbit = orbit

    def roll(self, ndice, modifier):
        return self.roller.roll(ndice, modifier)

    def get_volcanic_bonus(self):
        if self.get_type() == 'Sulfur':
            return 60
        if self.parent.type() == "Gas Giant":
            return 5
        return 0

    def make_orbit(self):
        """
        Randomly generate the orbit of this satellite, distinguishing between
        parent planets that are terrestrial or gas giants.
        """
        ptype = self.parent.type()
        if ptype == 'Terrestrial':
            # Check for size difference and infer roll bonus from it
            psize = SizeToInt[self.parent.get_size()]
            osize = SizeToInt[self.get_size()]
            diff = psize - osize
            bonus = 0
            if diff == 2:
                bonus = 2
            if diff == 1:
                bonus = 4
            dice = self.roll(2, bonus)
            self.__orbit = dice * 2.5 * self.parent.get_diameter()
        if ptype == 'Gas Giant':
            roll = self.roll(3, 3)
            if roll >= 15:
                roll += self.roll(2, 0)
            self.__orbit = roll / 2. * self.parent.get_diameter()

    def get_orbit(self):
        return self.__orbit

    def make_period(self):
        m1 = self.get_mass()
        mp = self.parent.get_mass()
        m = m1 + mp
        orbit = self.get_orbit()
        self.__period = 0.166 * (orbit ** 3 / m) ** 0.5

    def get_period(self):
        return self.__period

    def make_tidals(self):
        m = self.parent.get_mass()
        d = self.get_diameter()
        r = self.get_orbit()
        tidal = 2230000 * m * d / r ** 3
        tte = tidal * self.primary_star.get_age() / m
        self.__tte = round(tte)

    def get_total_tidal_effect(self):
        return self.__tte

    def make_rotation(self):
        if self.get_total_tidal_effect() > 50:
            rotperiod = self.get_period()  # [d]
        else:
            if self.get_size() == 'Large':
                bonus = 6
            if self.get_size() == 'Standard':
                bonus = 10
            if self.get_size() == 'Small':
                bonus = 14
            if self.get_size() == 'Tiny':
                bonus = 18
            diceroll = self.roll(3, bonus)
            rotperiod = (diceroll + self.get_total_tidal_effect()) / 24.
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
            if rotperiod > self.get_period():
                rotperiod = self.get_period()
        if self.roll(3, 0) >= 17:
            rotperiod = -rotperiod
        self.__rotperiod = rotperiod

    def get_rotation(self):
        return self.__rotperiod

    def make_calendar(self):
        # Calculate apparent length of a day for this moon
        s = self.parent.get_period() * 365.26  # [d]
        r = self.get_rotation()  # [d]
        if s == r:
            alen = None
        else:
            alen = s * r / (s - r)
        self.__alenday = alen

        # Calculate the time in which the planet can be seen
        s = self.get_period()  # [d]
        if s == r:
            alen = None
        else:
            alen = s * r / (s - r)
        self.__alenplanet = alen

    def get_day_length(self):
        return self.__alenday

    def get_planet_length(self):
        return self.__alenplanet

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_number(self, number):
        self.__number = number

    def getNumber(self):
        return self.__number


class Moonlet:
    def roll(self, ndice, modifier):
        return self.roller.roll(ndice, modifier)

    def __init__(self, parentplanet, family=None):
        self.parent = parentplanet
        self.roller = GD.DiceRoller()
        self.family = family
        self.make_orbit()
        self.make_period()

    def print_info(self):
        print("Moonlet Information")
        print("Parent Planet:\t{}".format(self.parent))
        print("        Orbit:\t{} Earth Diameters".format(self.get_orbit()))
        print("      Orb Per:\t{} d".format(self.get_period()))

    def make_orbit(self):
        ptype = self.parent.type()
        if ptype == 'Gas Giant' and self.family == 'first':
            self.__orbit = self.roll(1, 4) / 4. * self.parent.get_diameter()
        if ptype == 'Gas Giant' and self.family == 'third':
            # Make random orbits between 20 and 200 planetary diameters
            import random as r
            multiplier = r.uniform(20, 200)
            self.__orbit = multiplier * self.parent.get_diameter()

        if ptype == 'Terrestrial':
            self.__orbit = self.roll(1, 4) / 4. * self.parent.get_diameter()

    def get_orbit(self):
        return self.__orbit

    def make_period(self):
        m = self.parent.get_mass()
        orbit = self.get_orbit()
        self.__period = 0.166 * (orbit ** 3 / m) ** 0.5

    def get_period(self):
        return self.__period
