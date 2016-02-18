from .orbitcontents import OrbitContent
from .satellites import Moon, Moonlet
from .tables import GGSizeTable


class GasGiant(OrbitContent):

    def __init__(self, primary, orbitalradius, rollbonus=True):
        OrbitContent.__init__(self, primary, orbitalradius)
        self.size = self.make_size(rollbonus)
        self.mass, self.density = self.make_mass()
        self.diameter = self.make_diameter()
        self.cloudtop_gravity = self.make_cloudtop_gravity()
        # TODO: Can't these be collapsed into the semantically clearer Moons and Moonlets?
        self.first_family, self.second_family, self.third_family = self.make_moons()

    def __repr__(self):
        return repr("{} Gas Giant".format(self.size))

    def make_size(self, rollbonus) -> str:
        if rollbonus:
            modifier = 4
        else:
            modifier = 0
        dice = self.roller.roll_dice(3, modifier)
        size = "Small"
        if dice > 10:
            size = "Medium"
        if dice > 16:
            size = "Large"

        return size

    def print_info(self):
        print("---- Gas Giant {} Properties ----".format(self.get_angled_name()))
        print("     Size:\t{}".format(self.size))
        print("  BB Temp:\t{}".format(self.get_blackbody_temp()))
        print("     Mass:\t{}".format(self.mass))
        print("     Dens:\t{}".format(self.density))
        print("     Diam:\t{}".format(self.diameter))
        print("  Orb Per:\t{}".format(self.get_period()))
        print("  Orb Ecc:\t{}".format(self.get_eccentricity()))
        print(" Cl Top G:\t{}".format(self.cloudtop_gravity))
        print("  # 1st M:\t{}".format(len(self.first_family)))
        print("  # 2nd M:\t{}".format(len(self.second_family)))
        print("  # 3rd M:\t{}".format(len(self.third_family)))
        for moon in self.second_family:
            moon.print_info()
        print("------------------------------\n")

    def type(self):
        return "Gas Giant"

    def make_moons(self):
        first_family = self.make_first_family()
        second_family = self.make_second_family()
        third_family = self.make_third_family()
        return first_family, second_family, third_family

    def make_first_family(self) -> list:
        orbit = self.get_orbit()
        modifier = 0
        if orbit <= 0.1:
            modifier = -10
        if 0.1 < orbit <= 0.5:
            modifier = -8
        if 0.5 < orbit <= 0.75:
            modifier = -6
        if 0.75 < orbit <= 1.5:
            modifier = -3
        num_moonlets = self.roller.roll_dice(2, modifier)
        return [Moonlet(self, 'first') for _ in range(num_moonlets)]

    def make_second_family(self) -> list:
        orbit = self.get_orbit()
        modifier = 0
        if orbit <= 0.1:
            modifier = -200  # Equivalent to "do not roll"
        if 0.1 < orbit <= 0.5:
            modifier = -5
        if 0.5 < orbit <= 0.75:
            modifier = -3
        if 0.75 < orbit <= 1.5:
            modifier = -1
        num_moons = self.roller.roll_dice(1, modifier)
        return sorted([Moon(self, self.primary_star) for _ in range(num_moons)], key=lambda moon: moon.get_orbit())

    def make_third_family(self) -> list:
        orbit = self.get_orbit()
        modifier = 0
        if orbit <= 0.5:
            modifier = -200  # Equivalent to "do not roll"
        if 0.5 < orbit <= 0.75:
            modifier = -5
        if 0.75 < orbit <= 1.5:
            modifier = -4
        if 1.5 < orbit <= 3:
            modifier = -1
        num_moonlets = self.roller.roll_dice(1, modifier)
        return [Moonlet(self, 'third') for _ in range(num_moonlets)]

    def make_mass(self) -> tuple:
        size = self.get_size()
        diceroll = self.roller.roll_dice(3, 0)
        return GGSizeTable[size][diceroll]

    def get_mass(self):
        return self.mass

    def make_diameter(self) -> float:
        return (self.mass / self.density) ** (1 / 3.)

    def get_diameter(self):
        return self.diameter

    def make_cloudtop_gravity(self) -> float:
        return self.density * self.diameter

    def num_moons(self):
        return len(self.second_family)

    def num_moonlets(self):
        return len(self.first_family) + len(self.third_family)

    def set_number(self, number):
        OrbitContent.set_number(self, number)
        # Name the moons
        counter = 0
        for moon in self.second_family:
            counter += 1
            moon.set_number(counter)
            letter = self.primary_star.get_letter()
            name = '{}-{}-{}'.format(letter, number, counter)
            moon.set_name(name)

    def get_moons(self):
        return self.second_family

    def get_density(self):
        return self.density

    def get_gravity(self):
        return self.cloudtop_gravity

    def get_first_family(self):
        return self.first_family

    def get_third_family(self):
        return self.third_family
