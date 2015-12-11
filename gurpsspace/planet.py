from .world import World
from .satellites import Moon, Moonlet
from .tables import SizeToInt


class Planet(World):
    def __init__(self, primary, orbitalradius, sizeclass):
        World.__init__(self, primary, orbitalradius, sizeclass)
        self.generate_moons()
        self.make_tidals()
        self.make_rotation()
        self.make_volcanism()
        self.make_tectonism()
        self.make_resources()
        self.make_habitability()
        self.make_affinity()
        self.make_calendar()
        self.make_axial_tilt()

    def print_info(self):
        print("--- Planet {} Info ---".format(self.get_angled_name()))
        print("        Orbit:\t{}".format(self.get_orbit()))
        print("   World Type:\t{} ({})".format(self.get_size(), self.get_type()))
        if self.__nummoons > 0:
            print("      # Moons:\t{}".format(self.__nummoons))
            for moon in self.__moons:
                moon.print_info()
        if self.__nummoonlets > 0:
            print("    # Moonlets:\t{}".format(self.__nummoonlets))
        self.print_atmosphere()
        print("  Hydrogr Cov:\t{}".format(self.get_hydrographic_cover()))
        print("    Av Surf T:\t{}".format(self.get_average_surface_temp()))
        print("      Climate:\t{}".format(self.get_climate()))
        print("      Density:\t{}".format(self.get_density()))
        print("     Diameter:\t{}".format(self.get_diameter()))
        print("    Surf Grav:\t{}".format(self.get_gravity()))
        print("         Mass:\t{}".format(self.get_mass()))
        print("     Pressure:\t{} ({})".format(self.get_pressure(), self.get_pressure_category()))
        print("    Volcanism:\t{}".format(self.get_volcanism()))
        print("    Tectonics:\t{}".format(self.get_tectonics()))
        print("          RVM:\t{}".format(self.get_rvm()))
        print("       Res. V:\t{}".format(self.get_resources()))
        print(" Habitability:\t{}".format(self.get_habitability()))
        print("     Affinity:\t{}".format(self.get_affinity()))
        print("     Orb Per.:\t{}".format(self.get_period()))
        print("     Orb Ecc.:\t{}".format(self.get_eccentricity()))
        print("          TTE:\t{}".format(self.get_total_tidal_effect()))
        print("     Rot Per.:\t{} d".format(self.get_rotation()))
        print("      Day Len:\t{} d".format(self.get_day_length()))
        if self.get_moon_lengths() is not None:
            print("     Moon Len:\t{} d".format(self.get_moon_lengths()))
        print("      Ax Tilt:\t{}".format(self.get_axial_tilt()))
        print("------------------- \n")

    def print_atmosphere(self):
        atcomp = self.atmcomp
        bmarg, marg = self.get_marginal()
        atmcomp = [key for key in atcomp.keys() if atcomp[key] is True]
        if len(atmcomp) > 0:
            print("     Atm Comp:\t{}".format(atmcomp))
        if bmarg:
            print("     Marginal:\t{}".format(marg))

    def __repr__(self):
        return repr("{} Terrestrial Planet".format(self.get_size()))

    def type(self):
        return "Terrestrial"

    def generate_moons(self):
        roll_mod = -4
        roll_mod += self.moon_roll_modifier()
        moon_roll = self.roll(1, roll_mod)
        if moon_roll <= 0:
            # If we have no major moons, generate moonlets
            self.generate_moonlets()
        else:
            self.__nummoonlets = 0
            self.__moonlets = []
        self.__nummoons = moon_roll
        self.__moons = sorted([Moon(self, self.primary_star) for moonnum in range(moon_roll)], key=lambda moon: moon.get_orbit())

    def generate_moonlets(self):
        roll_mod = -2
        roll_mod += self.moon_roll_modifier()
        moonlet_roll = self.roll(1, roll_mod)
        self.__nummoonlets = moonlet_roll
        self.__moonlets = [Moonlet(self) for moonletnum in range(moonlet_roll)]

    def moon_roll_modifier(self):
        modifier = 0
        orbit = self.get_orbit()
        if orbit <= 0.5:
            return -20  # Equivalent to "do not roll"
        if 0.5 < orbit <= 0.75:
            modifier -= 3
        if 0.75 < orbit <= 1.5:
            modifier -= 1
        modifier += (SizeToInt[self.get_size()] - 2)
        return modifier

    def get_satellites(self):
        if self.__nummoons > 0:
            return self.__moons
        if self.__nummoonlets > 0:
            return self.__moonlets

    def get_volcanic_bonus(self):
        if self.__nummoons == 1:
            return 5
        if self.__nummoons > 1:
            return 10
        return 0

    def get_tectonic_bonus(self):
        if self.__nummoons == 1:
            return 2
        if self.__nummoons > 1:
            return 4
        return 0

    def make_tidals(self):
        # Collect tidal effects for Moons
        moon_tide = 0
        if self.__nummoons > 0:
            moons = self.get_satellites()
            for moon in moons:
                m = moon.get_mass()
                r = moon.get_orbit()
                d = self.get_diameter()
                moon_tide += 2230000 * m * d / r ** 3
        # Make tidal effect for star
        sun_mass = self.primary_star.get_mass()
        diameter = self.get_diameter()
        orbit = self.get_orbit()
        star_tide = 0.46 * sun_mass * diameter / orbit ** 3
        total_tide = (moon_tide + star_tide) * self.primary_star.get_age() / self.get_mass()
        self.__tte = round(total_tide)

    def get_total_tidal_effect(self):
        return self.__tte

    def make_rotation(self):
        if self.get_total_tidal_effect() > 50:
            if self.__nummoons == 0:
                rotational_period = self.get_period() * 365.26
            else:
                # Find innermost moon and its orbital period
                moons = sorted(self.get_satellites(), key=lambda moon: moon.get_orbit())
                inner_moon = moons[0]
                rotational_period = inner_moon.get_period()
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
            rotational_period = (diceroll + self.get_total_tidal_effect()) / 24.
            if rotational_period > 1.5 or diceroll - bonus >= 16:
                roll2 = self.roll(2, 0)
                if roll2 == 7:
                    rotational_period = self.roll(1, 0) * 2
                if roll2 == 8:
                    rotational_period = self.roll(1, 0) * 5
                if roll2 == 9:
                    rotational_period = self.roll(1, 0) * 10
                if roll2 == 10:
                    rotational_period = self.roll(1, 0) * 20
                if roll2 == 11:
                    rotational_period = self.roll(1, 0) * 50
                if roll2 == 12:
                    rotational_period = self.roll(1, 0) * 100
            if rotational_period > self.get_period() * 365.26:
                rotational_period = self.get_period() * 365.26
        if self.roll(3, 0) >= 13:
            rotational_period = -rotational_period
        self.__rotperiod = rotational_period

    def get_rotation(self):
        return self.__rotperiod

    def make_calendar(self):
        """Make the local calendar, including:

            - Apparent length of day
            - Apparent length of moon cycles
        """
        s = self.get_period() * 365.26
        r = self.get_rotation()
        if s == r:
            alen = None
        else:
            alen = s * r / (s - r)
        self.__daylength = alen

        if self.__nummoons > 0:
            self.__moonlength = []
            for moon in self.get_satellites():
                s = moon.get_period()
                if s == r:
                    alen = None
                else:
                    alen = s * r / (s - r)
                self.__moonlength.append(alen)

    def get_day_length(self):
        return self.__daylength

    def get_moon_lengths(self):
        if self.__nummoons > 0:
            return self.__moonlength
        else:
            return None

    def make_axial_tilt(self):
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

    def get_axial_tilt(self):
        return self.__axtilt

    def num_moons(self):
        return self.__nummoons

    def num_moonlets(self):
        return self.__nummoonlets

    def set_number(self, number):
        World.set_number(self, number)
        # Name the moons
        counter = 0
        for moon in self.__moons:
            counter += 1
            moon.set_number(counter)
            letter = self.primary_star.get_letter()
            name = '{}-{}-{}'.format(letter, number, counter)
            moon.set_name(name)
