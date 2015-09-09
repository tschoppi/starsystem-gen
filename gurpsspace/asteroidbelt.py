from .orbitcontents import OrbitContent
from .tables import world_climate


class AsteroidBelt(OrbitContent):
    """Class for asteroid belts."""
    def __init__(self, primarystar, orbitalradius):
        OrbitContent.__init__(self, primarystar, orbitalradius)
        self.make_resources()
        self.make_surface_temp()
        self.make_climate()
        self.__habitability = 0
        self.__affinity = self.__habitability + self.__rvm

    def __repr__(self):
        return repr("Asteroid Belt")

    def type(self):
        return "Ast. Belt"

    def print_info(self):
        print("Asteroid Belt {}".format(self.get_name()))
        print("    Orbit:\t{}".format(self.get_orbit()))
        print("  Orb Per:\t{}".format(self.get_period()))
        print("  Orb Ecc:\t{}".format(self.get_eccentricity()))
        print("      RVM:\t{}".format(self.__rvm))
        print("   Res. V:\t{}".format(self.__resources))
        print("     Aff.:\t{}".format(self.__affinity))
        print("")

    def make_resources(self):
        dice = self.roll(3, 0)
        rvm = -5
        value = 'Worthless'
        if dice == 4:
            rvm = -4
            value = 'Very Scant'
        if dice == 5:
            rvm = -3
            value = 'Scant'
        if 6 <= dice <= 7:
            rvm = -2
            value = 'Very Poor'
        if 8 <= dice <= 9:
            rvm = -1
            value = 'Poor'
        if 10 <= dice <= 11:
            rvm = 0
            value = 'Average'
        if 12 <= dice <= 13:
            rvm = 1
            value = 'Abundant'
        if 14 <= dice <= 15:
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

    def make_surface_temp(self):
        self.__avsurf = self.get_blackbody_temp() * 0.97

    def get_average_surface_temp(self):
        return self.__avsurf

    def make_climate(self):
        self.__climate = world_climate(self.get_average_surface_temp())

    def get_climate(self):
        return self.__climate

    def get_resources(self):
        return self.__resources

    def get_rvm(self):
        return self.__rvm

    def get_affinity(self):
        return self.__affinity
