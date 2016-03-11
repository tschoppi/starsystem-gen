from .orbitcontents import OrbitContent
from .tables import MAtmoTable, TempFactor, world_climate
from .tables import SizeConstraintsTable, pressure_category
from math import floor


class World(OrbitContent):
    def __init__(self, primary, orbitalradius, sizeclass):
        OrbitContent.__init__(self, primary, orbitalradius)
        self.__sizeclass = sizeclass
        self.type = self.make_type()
        self.make_atmosphere()
        self.__hydrocover = self.make_hydrographics()
        self.__averagesurface, self.__climatetype = self.make_climate()
        self.__density = self.make_density()
        self.__diameter = self.make_diameter()
        self.__surfacegravity = self.make_gravity()
        self.__mass = self.make_mass()
        self.make_pressure()
        self.make_volcanism()
        self.habitability = self.make_habitability()
        self.affinity = self.make_affinity()
        self.rvm, self.resources = self.make_resources()
        self.settlement_type = self.make_settlement_type()
        self.tech_level = self.make_tech_level()
        self.population = self.make_population(self.setting, self.setting.generate_race())
        self.population_rating = self.make_population_rating()

    def __repr__(self):
        return repr("World")

    def type(self) -> str:
        return "World"

    def get_size(self) -> str:
        return self.__sizeclass

    def make_type(self) -> str:
        """
        Determine and set the world type, according to blackbody temperature, size and primary star.
        """
        blackbody_temp = self.get_blackbody_temp()
        size = self.get_size()
        primary_star_mass = self.primary_star.get_mass()
        world_type = 'Ice'
        if size == 'Tiny' and blackbody_temp >= 141:
            world_type = 'Rock'
        if size == 'Small':
            if blackbody_temp <= 80:
                world_type = 'Hadean'
            if blackbody_temp >= 141:
                world_type = 'Rock'
        if size == 'Standard':
            if blackbody_temp <= 80:
                world_type = 'Hadean'
        if size == 'Standard' or size == 'Large':
            if 150 < blackbody_temp <= 230 and primary_star_mass <= 0.65:
                world_type = 'Ammonia'
            if 240 < blackbody_temp <= 320:
                age = self.primary_star.get_age()
                if size == 'Standard':
                    cap = 10
                if size == 'Large':
                    cap = 5
                bonus = floor(age / 0.5)
                if bonus > cap:
                    bonus = cap
                dice = self.roller.roll_dice(3, bonus)
                if dice >= 18:
                    world_type = 'Garden'
                else:
                    world_type = 'Ocean'
            if 320 < blackbody_temp <= 500:
                world_type = 'Greenhouse'
            if blackbody_temp > 500:
                world_type = 'Chthonian'
        return world_type

    def get_type(self) -> str:
        return self.type

    def get_atmospheric_mass(self):
        """
        :rtype: int | float
        """
        return self.__atmmass

    def make_atmosphere(self) -> None:
        """
        Determine details about the atmosphere and store them.
        """
        # TODO: Untangle this mess and get rid of the side effects
        size = self.get_size()
        type = self.get_type()
        # Determine atmospheric mass
        if size == 'Tiny' or type == 'Hadean' or type == 'Chthonian' or type == 'Rock':
            self.__atmmass = 0
        else:
            self.__atmmass = self.roller.roll_dice(3, 0) / 10.

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
            if self.roller.roll_dice(3, 0) > 15:
                self.atmcomp['Lethally Toxic'] = True
            else:
                self.atmcomp['Mildly Toxic'] = True

        if type == 'Ammonia' or type == 'Greenhouse':
            self.atmcomp['Suffocating'] = True
            self.atmcomp['Lethally Toxic'] = True
            self.atmcomp['Corrosive'] = True

        if type == 'Garden':
            if self.roller.roll_dice(3, 0) >= 12:
                self.__hasmarginal = True
                self.__marginal = MAtmoTable[self.roller.roll_dice(3, 0)]

        if size == 'Standard' and (type == 'Ice' or type == 'Ocean'):
            self.atmcomp['Suffocating'] = True
            if self.roller.roll_dice(3, 0) > 12:
                self.atmcomp['Mildly Toxic'] = True

        if size == 'Large' and (type == 'Ice' or type == 'Ocean'):
            self.atmcomp['Highly Toxic'] = True
            self.atmcomp['Suffocating'] = True

    def get_marginal(self) -> (bool, str):
        """
        Returns a tuple of bool and atmosphere.
        """
        return self.__hasmarginal, self.__marginal

    def make_hydrographics(self) -> int:
        hydro = 0
        size = self.get_size()
        type = self.get_type()
        if size == 'Small' and type == 'Ice':
            hydro = self.roller.roll_dice(1, 2) * 10
        if type == 'Ammonia':
            hydro = self.roller.roll_dice(2, 0) * 10
            if hydro > 100:
                hydro = 100
        if type == 'Ice' and (size == 'Standard' or size == 'Large'):
            hydro = self.roller.roll_dice(2, -10) * 10
        if type == 'Ocean' or type == 'Garden':
            bonus = 4
            if size == 'Large':
                bonus = 6
            hydro = self.roller.roll_dice(1, bonus) * 10
            if hydro > 100:
                hydro = 100
        if type == 'Greenhouse':
            hydro = self.roller.roll_dice(2, -7) * 10
        # Introduce a small amount of randomness to the hydrographic coverage,
        # to make the worlds more varied and to make them feel more real
        # Do this only if there is any surface liquid at all,
        # avoiding those astral bodies who cannot have a hydrographic coverage at all
        # Vary by +- 5% as described in the rule book
        if 10 <= hydro <= 90:
            sign = self.roller.roll_dice(1, 0, 2)
            variation = self.roller.roll_dice(1, 0, 5)
            if sign == 1:
                hydro += variation
            else:
                hydro -= variation

        return hydro

    def get_hydrographic_cover(self) -> int:
        return self.__hydrocover

    def get_absorption_greenhouse(self) -> (int, int):
        """
        Return a tuple (absorption factor, greenhouse factor) based on world
        type and size.
        """
        world_type = self.get_type()
        size = self.get_size()
        if world_type is not 'Garden' and world_type is not 'Ocean':
            return TempFactor[world_type][size]
        else:
            hydro = self.get_hydrographic_cover()
            absorption = 0.84
            if hydro <= 90:
                absorption = 0.88
            if hydro <= 50:
                absorption = 0.92
            if hydro <= 20:
                absorption = 0.95
            return absorption, 0.16

    def make_climate(self) -> tuple:
        # TODO: Refactor by assigning better names
        abs, green = self.get_absorption_greenhouse()
        matm = self.get_atmospheric_mass()
        bbcorr = abs * (1 + (matm * green))

        return bbcorr * self.get_blackbody_temp(), world_climate(self.__averagesurface)

    def get_average_surface_temp(self):
        return self.__averagesurface

    def get_climate(self) -> str:
        return self.__climatetype

    def make_density(self) -> float:
        type = self.get_type()
        size = self.get_size()
        density = 0
        dice = self.roller.roll_dice(3, 0)
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
        return density

    def get_density(self):
        """
        :rtype: int | float
        """
        return self.__density

    def make_diameter(self) -> float:
        size = self.get_size()
        bb = self.get_blackbody_temp()
        dens = self.get_density()
        smin, smax = SizeConstraintsTable[size]
        term = (bb / dens) ** (0.5)
        min = term * smin
        max = term * smax
        diff = max - min
        diam = self.roller.roll_dice(2, -2) * 0.1 * diff + min
        return diam

    def get_diameter(self):
        return self.__diameter

    def make_gravity(self) -> float or int:
        return self.get_density() * self.get_diameter()

    def get_gravity(self) -> float or int:
        return self.__surfacegravity

    def make_mass(self) -> float or int:
        return self.get_density() * self.get_diameter() ** 3

    def get_mass(self) -> float or int:
        return self.__mass

    def make_pressure(self) -> tuple:
        size = self.get_size()
        type = self.get_type()
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
            pressure = self.get_mass() * factor * self.get_gravity()
            category = pressure_category(pressure)
        return pressure, category

    def get_pressure(self):
        return self.__pressure

    def get_pressure_category(self):
        return self.__presscat

    def make_volcanism(self):
        bonus = round(self.get_gravity() / self.primary_star.get_age() * 40)
        bonus += self.get_volcanic_bonus()
        volcanoroll = self.roller.roll_dice(3, bonus)
        activity = 'None'
        if volcanoroll > 16:
            activity = 'Light'
        if volcanoroll > 20:
            activity = 'Moderate'
        if volcanoroll > 26:
            activity = 'Heavy'
        if volcanoroll > 70:
            activity = 'Extreme'
        return activity

    def get_volcanism(self):
        return self.__volcanism

    def get_volcanic_bonus(self):
        return 0

    def make_tectonism(self):
        if self.get_size() == 'Small' or self.get_size() == 'Tiny':
            return 'None'
        else:
            volc = self.get_volcanism()
            bonus = 0
            if volc == 'None':
                bonus -= 8
            if volc == 'Light':
                bonus -= 4
            if volc == 'Heavy':
                bonus += 4
            if volc == 'Extreme':
                bonus += 8
            if self.get_hydrographic_cover() < 50:
                bonus -= 2
            bonus += self.get_tectonic_bonus()
            tect = self.roller.roll_dice(3, bonus)
            activity = 'None'
            if tect > 6:
                activity = 'Light'
            if tect > 10:
                activity = 'Moderate'
            if tect > 14:
                activity = 'Heavy'
            if tect > 18:
                activity = 'Extreme'
            return activity

    def get_tectonic_bonus(self):
        return 0

    def get_tectonics(self):
        return self.__tectonic

    def get_resourcebonus(self):
        volc = self.get_volcanism()
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

    def make_resources(self):
        rollbonus = self.get_resourcebonus()
        dice = self.roller.roll_dice(3, rollbonus)
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
        if dice > 18:
            rvm = 3
            value = 'Rich'
        return rvm, value

    def get_rvm(self):
        return self.rvm

    def get_resources(self):
        return self.resources

    def make_habitability(self):
        modifier = 0
        # The following is from p. 121
        volc = self.get_volcanism()
        tect = self.get_tectonics()
        if volc == 'Heavy':
            modifier -= 1
        if volc == 'Extreme':
            modifier -= 2
        if tect == 'Heavy':
            modifier -= 1
        if tect == 'Extreme':
            modifier -= 2

        # Now comes standard implementation, p. 88
        # First: Based on breathable or non-breathable atmosphere
        atmo = [key for key in self.atmcomp.keys() if self.atmcomp[key] is True]
        if len(atmo) > 0:
            # Non-breathable atmosphere
            if len(atmo) == 2:
                # Suffocating and Toxic
                modifier -= 1
            elif len(atmo) == 3:
                # Suffocating, Toxic and Corrosive
                modifier -= 2
        else:
            # Breathable atmosphere
            press = self.get_pressure_category()
            if press == 'Very Thin':
                modifier += 1
            if press == 'Thin':
                modifier += 2
            if press == 'Standard' or press == 'Dense':
                modifier += 3
            if press == 'Very Dense' or press == 'Superdense':
                modifier += 1
            hasmarg, marg = self.get_marginal()
            if not hasmarg:
                modifier += 1
            climate = self.get_climate()
            if climate == 'Cold' or climate == 'Hot':
                modifier += 1
            if climate in ['Chilly', 'Cool', 'Normal', 'Warm', 'Tropical']:
                modifier += 2
        # Now the Hydrographics Coverage conditions
        if self.get_type() in ['Garden', 'Ocean']:
            hydro = self.get_hydrographic_cover()
            if (0 < hydro < 60) or (90 < hydro < 100):
                modifier += 1
            elif hydro > 0:
                modifier += 2

        # Check lower bounds (p. 121)
        if modifier < -2:
            modifier = -2
        return modifier

    def get_habitability(self):
        return self.habitability

    def make_affinity(self):
        return self.get_rvm() + self.get_habitability()

    def get_affinity(self):
        return self.affinity

    def make_settlement_type(self):
        # TODO: Check if space has been claimed / generate societies which could claim space
        if self.get_affinity() > 0:
            return "Colony"
        else:
            return "Outpost"

    def get_settlement_type(self) -> str:
        return self.settlement_type

    def make_tech_level(self):

        # TODO: Make TL a global setting and actually calculate the TL here
        # TODO: Check for TL8 if habitability <= 3
        modifier = 0
        if self.get_settlement_type() == "Homeworld (Non-Spacefaring)":
            modifier += -10

        if self.get_settlement_type() == "Homeworld" or "Colony":
            if 4 <= self.get_habitability() <= 6:
                modifier += 1
            if self.get_habitability() <= 3:
                modifier += 2

        if self.get_settlement_type() == "Outpost" and self.get_habitability() <= 3:
            modifier += 3

        roll = self.roller.roll(3, modifier)
        if roll == 3:
            return "Primitive", 1
        elif roll == 4:
            return "Standard - 3", self.setting.tech_level - 3
        elif roll == 5:
            return "Standard - 2", self.setting.tech_level - 2
        elif 6 <= roll <= 7:
            return "Standard - 1", self.setting.tech_level - 1
        elif 8 <= roll <= 11:
            return "Standard (Delayed)", self.setting.tech_level
        elif 12 <= roll <= 15:
            return "Standard", self.setting.tech_level
        else:
            return "Standard (Advanced)", self.setting.tech_level

    def make_population(self, setting, race):
        if self.get_settlement_type() == "Outpost":
            return self.make_outpost_population()
        else:
            # if self.get_habitability() <= 3 and tech_level <= 7: self.population = 0 Set settlement to uninhabited!
            base_capacity = self.get_carrying_capacity_by_tech_level()
            base_capacity *= self.get_diameter() ** 2
            base_capacity *= self.get_affinity_population_modifier()
            if setting.tech_level < 8 and race.is_carnivore:
                base_capacity /= 10
            for _ in range(race.increased_consumption):
                base_capacity /= 2
            if race.reduced_consumption > 0:
                multipliers = [1.5, 3, 10]
                base_capacity *= multipliers[race.reduced_consumption]

            if self.get_settlement_type() == "Homeworld" and setting.tech_level < 5:
                return round(base_capacity * (self.roller.roll(2, -3) / 10))
            if self.get_settlement_type() == "Homeworld" and setting.tech_level >= 5:
                return round(base_capacity * (10 / self.roller.roll(2, 0)), 2)

            # In case of colony:
            if self.get_settlement_type() == "Colony":
                modified_roll = self.roller.roll(3, 0) + (3 * self.get_affinity())  # + 1 per 10 yrs of colony age
                progression = [10, 13, 15, 20, 25, 30, 40, 50, 60, 80]
                multiplier = 1000
                while modified_roll > 10:
                    modified_roll -= 10
                    multiplier *= 10
                return round(progression[modified_roll % 10] * multiplier, 2)

    def get_carrying_capacity_by_tech_level(self, tech_level=0):
        # TODO: move this to a setting class?
        if tech_level == 0:
            return 10000
        elif tech_level == 1:
            return 100000
        elif tech_level == 2:
            return 500000
        elif tech_level == 3:
            return 600000
        elif tech_level == 4:
            return 700000
        elif tech_level == 5:
            return 2500000
        elif tech_level == 6:
            return 5000000
        elif tech_level == 7:
            return 7500000
        elif tech_level == 8:
            return 10000000
        elif tech_level == 9:
            return 15000000
        elif tech_level == 10:
            return 20000000
        else:
            # FIXME: This should be "GM option". How to handle that?
            return 50000000

    def make_population_rating(self) -> int:
        population = self.population
        pop_rating = 0
        while population >= 10:
            pop_rating += 1
            population /= 10
        return pop_rating

    def make_outpost_population(self):
        progression = [1, 1.5, 2.5, 4, 6]
        multiplier = 100
        roll = self.roller.roll(3, -3)  # Get one of 16 results between 0 and 15
        while roll > 4:
            roll -= 5
            multiplier *= 10

        adjustment = round(1 + (random.randint(-25, 25) / 100), 2)  # Generate an adjustment factor of +-25%
        return round(progression[roll % 5] * multiplier * adjustment, 2)

    def get_affinity_population_modifier(self):
        affinity = self.get_affinity()
        # progression here: 3, 6, 13, 25, 50, 100; except for middle bit, where it is [1,] 2, 4, 8, 15
        if affinity <= -5:
            return 0.03
        if affinity == -4:
            return 0.06
        if affinity == -3:
            return 0.13
        if affinity == -2:
            return 0.25
        if affinity == -1:
            return 0.5
        if affinity == 0:
            return 1
        if affinity == 1:
            return 2
        if affinity == 2:
            return 4
        if affinity == 3:
            return 8
        if affinity == 4:
            return 15
        if affinity == 5:
            return 30
        if affinity == 6:
            return 60
        if affinity == 7:
            return 130
        if affinity == 8:
            return 250
        if affinity == 9:
            return 500
        else:
            return 1000
