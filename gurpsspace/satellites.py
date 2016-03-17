from . import dice
from .world import World
from .tables import SizeToInt, IntToSize


class Moon(World):

    def __init__(self, parent_planet, primary_star):
        self.roller = dice.DiceRoller()
        self.parent = parent_planet
        self.primary_star = primary_star
        self._bbtemp = self.make_blackbody_temperature()
        self.orbit = None
        self._sizeclass = self.make_size()
        self._type = self.make_type()
        self.make_atmosphere()
        self._hydrocover = self.make_hydrographics()
        self._averagesurface, self._climatetype = self.make_climate()
        self._density = self.make_density()
        self._diameter = self.make_diameter()
        self._surfacegravity = self.make_gravity()
        self._mass = self.make_mass()
        self._pressure, self._presscat = self.make_pressure()
        self._volcanism = self.make_volcanism()
        self._tectonic = self.make_tectonism()
        self._rvm, self._resources = self.make_resources()
        self._habitability = self.make_habitability()
        self._affinity = self.make_affinity()
        self.orbit = self.make_orbit()
        self.period = self.make_period()
        self._tte = self.make_tidals()
        self._rotperiod = self.make_rotation()
        self._alenday = self.make_calendar()

    def print_info(self):
        print("         *** Moon {} Information *** ".format(self.get_angled_name()))
        # print("Parent Planet:\t{}".format(self.parent))
        print("           World Type:\t{} ({})".format(self._sizeclass, self.get_type()))
        print("                Orbit:\t{} Earth Diameters".format(self.orbit))
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
        return self.parent.get_blackbody_temp()

    def get_blackbody_temp(self):
        return self._bbtemp

    def make_size(self):
        parent = self.parent
        parentsize = SizeToInt[parent.get_size()]
        if parent.type() == "Gas Giant":
            parentsize = SizeToInt["Large"]
        diceroll = self.roller.roll_dice(3, 0)
        if diceroll >= 15:
            childsize = parentsize - 1
        if diceroll >= 12:
            childsize = parentsize - 2
        else:
            childsize = parentsize - 3
        if childsize < 0:
            childsize = 0
        return IntToSize[childsize]

    def get_size(self):
        return self._sizeclass

    def set_orbit(self, orbit):
        self.orbit = orbit

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
            dice = self.roller.roll_dice(2, bonus)
            return dice * 2.5 * self.parent.get_diameter()
        if ptype == 'Gas Giant':
            roll = self.roller.roll_dice(3, 3)
            if roll >= 15:
                roll += self.roller.roll_dice(2, 0)
            return roll / 2. * self.parent.get_diameter()

    def get_orbit(self):
        return self.orbit

    def make_period(self):
        """
        Calculate and return the orbital period
        """
        m1 = self.get_mass()
        mp = self.parent.get_mass()
        m = m1 + mp
        orbit = self.get_orbit()
        return 0.166 * (orbit ** 3 / m) ** 0.5

    def get_period(self):
        return self.period

    def make_tidals(self):
        """
        Calculate and return the total tidal effect (TTE)
        """
        m = self.parent.get_mass()
        d = self.get_diameter()
        r = self.get_orbit()
        tidal = 2230000 * m * d / r ** 3
        tte = tidal * self.primary_star.get_age() / m
        return round(tte)

    def get_total_tidal_effect(self):
        return self._tte

    def make_rotation(self):
        """
        Calculate and return the rotational period
        """
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
            diceroll = self.roller.roll_dice(3, bonus)
            rotperiod = (diceroll + self.get_total_tidal_effect()) / 24.
            if rotperiod > 1.5 or diceroll - bonus >= 16:
                roll2 = self.roller.roll_dice(2, 0)
                if roll2 == 7:
                    rotperiod = self.roller.roll_dice(1, 0) * 2
                if roll2 == 8:
                    rotperiod = self.roller.roll_dice(1, 0) * 5
                if roll2 == 9:
                    rotperiod = self.roller.roll_dice(1, 0) * 10
                if roll2 == 10:
                    rotperiod = self.roller.roll_dice(1, 0) * 20
                if roll2 == 11:
                    rotperiod = self.roller.roll_dice(1, 0) * 50
                if roll2 == 12:
                    rotperiod = self.roller.roll_dice(1, 0) * 100
            if rotperiod > self.get_period():
                rotperiod = self.get_period()
        if self.roller.roll_dice(3, 0) >= 17:
            rotperiod = -rotperiod
        return rotperiod

    def get_rotation(self):
        return self._rotperiod

    def make_calendar(self):
        """
        Calculate and return the apparent length of a day for this moon
        """
        s = self.parent.get_period() * 365.26  # [d]
        r = self.get_rotation()  # [d]
        if s == r:
            alen = None
        else:
            alen = s * r / (s - r)
        return alen

        # Calculate the time in which the planet can be seen
        s = self.get_period()  # [d]
        if s == r:
            alen = None
        else:
            alen = s * r / (s - r)
        self._alenplanet = alen

    def get_day_length(self):
        return self._alenday

    def get_planet_length(self):
        return self._alenplanet

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def get_angled_name(self):
        return "<" + self._name + ">"

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number


class Moonlet:

    def __init__(self, parentplanet, family=None):
        self.parent = parentplanet
        self.roller = dice.DiceRoller()
        self.family = family
        self._orbit = self.make_orbit()
        self._period = self.make_period()

    def print_info(self):
        print("Moonlet Information")
        print("Parent Planet:\t{}".format(self.parent))
        print("        Orbit:\t{} Earth Diameters".format(self.get_orbit()))
        print("      Orb Per:\t{} d".format(self.get_period()))

    def make_orbit(self):
        ptype = self.parent.type()
        if ptype == 'Gas Giant' and self.family == 'first':
            return self.roller.roll_dice(1, 4) / 4. * self.parent.get_diameter()
        if ptype == 'Gas Giant' and self.family == 'third':
            # Make random orbits between 20 and 200 planetary diameters
            import random as r
            multiplier = r.uniform(20, 200)
            return multiplier * self.parent.get_diameter()

        if ptype == 'Terrestrial':
            return self.roller.roll_dice(1, 4) / 4. * self.parent.get_diameter()

    def get_orbit(self):
        return self._orbit

    def make_period(self):
        m = self.parent.get_mass()
        orbit = self.get_orbit()
        return 0.166 * (orbit ** 3 / m) ** 0.5

    def get_period(self):
        return self._period
