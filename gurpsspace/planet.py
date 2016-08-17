from .world import World
from .satellites import Moon, Moonlet
from .tables import SizeToInt

from typing import Tuple, List, Union


class Planet(World):

    def __init__(self, primary, orbitalradius, sizeclass):
        World.__init__(self, primary, orbitalradius, sizeclass)
        self.nummoons, self.moons = self.generate_moons()
        if self.nummoons == 0:
            self.nummoonlets, self.moonlets = self.generate_moonlets()
        else:
            self.nummoonlets, self.moonlets = 0, []
        self.tte = self.make_tidals()
        self.rotperiod = self.make_rotation()
        self.volcanism = self.make_volcanism()
        self.tectonic = self.make_tectonism()
        self.rvm, self.resources = self.make_resources()
        self.habitability = self.make_habitability()
        self.affinity = self.make_affinity()
        self.daylength, self.moonlength = self.make_calendar()
        self.axtilt = self.make_axial_tilt()

    def print_info(self):
        print("--- Planet {} Info ---".format(self.get_angled_name()))
        print("        Orbit:\t{}".format(self.get_orbit()))
        print("   World Type:\t{} ({})".format(self.get_size(), self.get_type()))
        if self.nummoons > 0:
            print("      # Moons:\t{}".format(self.nummoons))
            for moon in self.moons:
                moon.print_info()
        if self.nummoonlets > 0:
            print("    # Moonlets:\t{}".format(self.nummoonlets))
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

    def generate_moons(self) -> Tuple[int, List]:
        roll_mod = -4
        roll_mod += self.moon_roll_modifier()
        moon_roll = self.roller.roll_dice(1, roll_mod)

        return moon_roll, sorted([Moon(self, self.primary_star) for _ in range(moon_roll)], key=lambda moon: moon.get_orbit())

    def generate_moonlets(self) -> Tuple[int, List]:
        roll_mod = -2
        roll_mod += self.moon_roll_modifier()
        moonlet_roll = self.roller.roll_dice(1, roll_mod)

        return moonlet_roll, [Moonlet(self) for _ in range(moonlet_roll)]

    def moon_roll_modifier(self) -> int:
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

    def get_satellites(self) -> List:
        if self.nummoons > 0:
            return self.moons
        if self.nummoonlets > 0:
            return self.moonlets

    def get_volcanic_bonus(self) -> int:
        if not hasattr(self, 'nummoons'):
            return 0
        if self.nummoons == 1:
            return 5
        if self.nummoons > 1:
            return 10
        return 0

    def get_tectonic_bonus(self) -> int:
        if self.nummoons == 1:
            return 2
        if self.nummoons > 1:
            return 4
        return 0

    def make_tidals(self) -> Union[float, int]:
        # Collect tidal effects for Moons
        moon_tide = 0
        if self.nummoons > 0:
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
        return round(total_tide)

    def get_total_tidal_effect(self):
        return self.tte

    def make_rotation(self) -> Union[float, int]:
        bonus = 0
        if self.get_total_tidal_effect() > 50:
            if self.nummoons == 0:
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
            diceroll = self.roller.roll_dice(3, bonus)
            rotational_period = (diceroll + self.get_total_tidal_effect()) / 24.
            if rotational_period > 1.5 or diceroll - bonus >= 16:
                roll2 = self.roller.roll_dice(2, 0)
                if roll2 == 7:
                    rotational_period = self.roller.roll_dice(1, 0) * 2
                if roll2 == 8:
                    rotational_period = self.roller.roll_dice(1, 0) * 5
                if roll2 == 9:
                    rotational_period = self.roller.roll_dice(1, 0) * 10
                if roll2 == 10:
                    rotational_period = self.roller.roll_dice(1, 0) * 20
                if roll2 == 11:
                    rotational_period = self.roller.roll_dice(1, 0) * 50
                if roll2 == 12:
                    rotational_period = self.roller.roll_dice(1, 0) * 100
            if rotational_period > self.get_period() * 365.26:
                rotational_period = self.get_period() * 365.26
        if self.roller.roll_dice(3, 0) >= 13:
            rotational_period = -rotational_period
        return rotational_period

    def get_rotation(self):
        return self.rotperiod

    def make_calendar(self) -> Tuple[float, List[float]]:
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
        day_length = alen

        moon_length = []
        if self.nummoons > 0:
            for moon in self.get_satellites():
                s = moon.get_period()
                if s == r:
                    alen = None
                else:
                    alen = s * r / (s - r)
                moon_length.append(alen)
        return day_length, moon_length

    def get_day_length(self):
        return self.daylength

    def get_moon_lengths(self) -> Union[List[float], None]:
        if self.nummoons > 0:
            return self.moonlength
        else:
            return None

    def make_axial_tilt(self) -> int:
        roll1 = self.roller.roll_dice(3, 0)
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
            roll2 = self.roller.roll_dice(1, 0)
            if roll2 in [1, 2]:
                base = 50
            if roll2 in [3, 4]:
                base = 60
            if roll2 == 5:
                base = 70
            if roll2 == 6:
                base = 80
        return base + self.roller.roll_dice(2, -2)

    def get_axial_tilt(self):
        return self.axtilt

    def num_moons(self):
        return self.nummoons

    def num_moonlets(self):
        return self.nummoonlets

    def set_number(self, number):
        World.set_number(self, number)
        # Name the moons
        counter = 0
        for moon in self.moons:
            counter += 1
            moon.set_number(counter)
            letter = self.primary_star.get_letter()
            name = '{}-{}-{}'.format(letter, number, counter)
            moon.set_name(name)
