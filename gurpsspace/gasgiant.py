from .orbitcontents import OrbitContent
from .satellites import Moon, Moonlet
from .tables import GGSizeTable


class GasGiant(OrbitContent):
    def __init__(self, primary, orbitalradius, rollbonus=True):
        OrbitContent.__init__(self, primary, orbitalradius)
        self.make_size(rollbonus)
        self.make_mass()
        self.make_diameter()
        self.make_cloudtop_gravity()
        self.make_moons()
        # self.print_info()

    def __repr__(self):
        return repr("{} Gas Giant".format(self.__size))

    def make_size(self, rollbonus):
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

    def get_size(self):
        return self.__size

    def print_info(self):
        print("---- Gas Giant {} Properties ----".format(self.get_angled_name()))
        print("     Size:\t{}".format(self.__size))
        print("  BB Temp:\t{}".format(self.get_blackbody_temp()))
        print("     Mass:\t{}".format(self.__mass))
        print("     Dens:\t{}".format(self.__density))
        print("     Diam:\t{}".format(self.__diameter))
        print("  Orb Per:\t{}".format(self.get_period()))
        print("  Orb Ecc:\t{}".format(self.get_eccentricity()))
        print(" Cl Top G:\t{}".format(self.__gravity))
        print("  # 1st M:\t{}".format(len(self.__firstfamily)))
        print("  # 2nd M:\t{}".format(len(self.__secondfamily)))
        print("  # 3rd M:\t{}".format(len(self.__thirdfamily)))
        for moon in self.__secondfamily:
            moon.print_info()
        print("------------------------------\n")

    def type(self):
        return "Gas Giant"

    def make_moons(self):
        self.make_first_family()
        self.make_second_family()
        self.make_third_family()

    def make_first_family(self):
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
        num_moonlets = self.roll(2, modifier)
        if num_moonlets < 0:
            num_moonlets = 0
        self.__firstfamily = [Moonlet(self, 'first') for nummoonlet in range(num_moonlets)]

    def make_second_family(self):
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
        num_moons = self.roll(1, modifier)
        if num_moons < 0:
            num_moons = 0
        self.__secondfamily = sorted([Moon(self, self.primary_star) for _ in range(num_moons)], key=lambda moon: moon.get_orbit())

    def make_third_family(self):
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
        num_moonlets = self.roll(1, modifier)
        if num_moonlets < 0:
            num_moonlets = 0
        self.__thirdfamily = [Moonlet(self, 'third') for _ in range(num_moonlets)]

    def make_mass(self):
        size = self.get_size()
        diceroll = self.roll(3, 0)
        mass, density = GGSizeTable[size][diceroll]
        self.__mass = mass
        self.__density = density

    def get_mass(self):
        return self.__mass

    def make_diameter(self):
        self.__diameter = (self.__mass / self.__density) ** (1 / 3.)

    def get_diameter(self):
        return self.__diameter

    def make_cloudtop_gravity(self):
        self.__gravity = self.__density * self.__diameter

    def num_moons(self):
        return len(self.__secondfamily)

    def num_moonlets(self):
        return len(self.__firstfamily) + len(self.__thirdfamily)

    def set_number(self, number):
        OrbitContent.set_number(self, number)
        # Name the moons
        counter = 0
        for moon in self.__secondfamily:
            counter += 1
            moon.set_number(counter)
            letter = self.primary_star.get_letter()
            name = '{}-{}-{}'.format(letter, number, counter)
            moon.set_name(name)

    def get_moons(self):
        return self.__secondfamily

    def get_density(self):
        return self.__density

    def get_gravity(self):
        return self.__gravity

    def get_first_family(self):
        return self.__firstfamily

    def get_third_family(self):
        return self.__thirdfamily
