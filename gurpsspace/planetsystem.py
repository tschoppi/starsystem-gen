from . import dice
from .gasgiant import GasGiant
from .asteroidbelt import AsteroidBelt
from .planet import Planet
from .tables import OrbitalSpace


class PlanetSystem:

    def __init__(self, parentstar):
        self.roller = dice.DiceRoller()
        self.parentstar = parentstar
        self.__innerlimit, self.__outerlimit = parentstar.get_orbit_limits()
        self.__snowline = parentstar.get_snowline()
        self.__primarylum = parentstar.get_luminosity()
        self.__forbidden = parentstar.has_forbidden_zone()
        if self.__forbidden:
            self.__innerforbidden, self.__outerforbidden = parentstar.get_forbidden_zone()
        self.make_gasgiant_arrangement()
        self.place_first_gasgiant()
        self.createorbits()
        self.make_content_list()
        self.place_gas_giants()
        self.fill_orbits()
        self.name_contents()
        self.make_eccentricities()

    def printinfo(self):
        print("--------------------")
        print(" Planet System Info ")
        print("--------------------")
        print("GG Arrngmnt:\t{}".format(self.__gasarrangement))
        # Nicely formatted first gas giant orbit
        nggorb = round(self.__firstgasorbit, 3)
        print("Frst GG Orb:\t{}".format(nggorb))
        # Nicely formatted orbits
        norb = [round(orb, 3) for orb in self.__orbitarray]
        print("     Orbits:\t{}".format(norb))
        # Beautifully formatted listing of orbits and contents
        self.printorbcontent()
        self.listorbcontentdetails()

    def printorbcontent(self):
        first = True
        for skey in sorted(self.__orbitcontents):
            if first:
                print("Orb Content:\t{}: {}".format(round(skey, 3), self.__orbitcontents[skey]))
                first = False
            else:
                print("\t\t{}: {}".format(round(skey, 3), self.__orbitcontents[skey]))

    def listorbcontentdetails(self):
        for skey in sorted(self.__orbitcontents):
            self.__orbitcontents[skey].print_info()

    def get_orbitcontents(self):
        return self.__orbitcontents

    def allowed_orbit(self, testorbit):
        result = testorbit >= self.__innerlimit
        result &= testorbit <= self.__outerlimit
        if self.__forbidden and result:
            result2 = testorbit <= self.__innerforbidden
            result2 |= testorbit >= self.__outerforbidden
            return result & result2
        else:
            return result

    def make_gasgiant_arrangement(self):
        dice = self.roller.roll_dice(3, 0)
        self.__gasarrangement = 'None'
        if dice > 10:
            self.__gasarrangement = 'Conventional'
        if dice > 12:
            self.__gasarrangement = 'Eccentric'
        if dice > 14:
            self.__gasarrangement = 'Epistellar'
        if self.__forbidden:
            if self.__snowline > self.__innerforbidden and self.__snowline < self.__outerforbidden:
                self.__gasarrangement = 'None'

    def place_first_gasgiant(self):
        orbit = 0
        if self.__gasarrangement == 'Conventional':
            orbit = (1 + (self.roller.roll_dice(2, -2) * 0.05)) * self.__snowline
        if self.__gasarrangement == 'Eccentric':
            orbit = self.roller.roll_dice(1, 0) * 0.125 * self.__snowline
        if self.__gasarrangement == 'Epistellar':
            orbit = self.roller.roll_dice(3, 0) * 0.1 * self.__innerlimit
        self.__firstgasorbit = orbit

    def createorbits(self):
        orbits = []
        if self.__gasarrangement == 'None':
            # Create orbits outwards from the innermost limit
            if self.__forbidden and self.__innerforbidden < self.__innerlimit:
                innermost = self.__outerforbidden
            else:
                innermost = self.__innerlimit
            orbits += [innermost]
            orbitsout = self.orbit_outward(innermost)
            orbits += orbitsout
        elif self.__gasarrangement == 'Epistellar':
            # Create orbits outwards. Since the epistellar GasGiant is closer to
            # the star than the inner orbital limit, special conditions apply
            orbits += [self.__firstgasorbit]
            startorbit = self.__firstgasorbit + 0.15
            # If the minimal distance is not within the orbital zone make the
            # next orbit right at the border
            if not self.allowed_orbit(startorbit):
                startorbit = self.__innerlimit
            orbits += [startorbit]
            orbitsout = self.orbit_outward(startorbit)
            orbits += orbitsout
        else:
            # Create orbits inwards then outwards from first gas giant
            orbits += [self.__firstgasorbit]
            orbitsin = self.orbit_inward(self.__firstgasorbit)
            orbitsout = self.orbit_outward(self.__firstgasorbit)
            orbits = orbitsin + orbits
            orbits += orbitsout
        self.__orbitarray = orbits

    def orbit_outward(self, startorbit):
        allowed = True
        orbits = []
        old_orbit = startorbit
        new_orbit = 0
        while (allowed):
            orbital_separation = OrbitalSpace[self.roller.roll_dice(3, 0)]
            new_orbit = old_orbit * orbital_separation
            if self.allowed_orbit(new_orbit) and new_orbit - old_orbit >= 0.15:
                orbits += [new_orbit]
                old_orbit = new_orbit
            else:
                allowed = False
                new_orbits = [old_orbit * 1.4, old_orbit * 2.0]
                success = False
                # Check 1.4 and 2.0 if allowed, take the first
                for possible_orbit in new_orbits:
                    if self.allowed_orbit(possible_orbit):
                        if possible_orbit - old_orbit >= 0.15:
                            success = True
                            new_orbit = possible_orbit
                            old_orbit = possible_orbit
                            break
                if success:
                    orbits += [new_orbit]
                    allowed = True
                else:
                    # If our searching yielded nothing, check if there is an
                    # allowed orbit with the minimal distance, and put that
                    if self.allowed_orbit(old_orbit + 0.15) and self.allowed_orbit(old_orbit * 1.4):
                        new_orbit = old_orbit + 0.15
                        orbits += [new_orbit]
                        old_orbit = new_orbit
                        allowed = True

        return orbits

    def orbit_inward(self, startorbit):
        allowed = True
        orbits = []
        oldorbit = startorbit
        neworbit = 0
        while (allowed):
            orbsep = OrbitalSpace[self.roller.roll_dice(3, 0)]
            neworbit = oldorbit / orbsep
            if self.allowed_orbit(neworbit) and oldorbit - neworbit >= 0.15:
                orbits = [neworbit] + orbits
                oldorbit = neworbit
            else:
                allowed = False
                # Check to fit one last orbit
                neworbit = oldorbit / 1.4
                if self.allowed_orbit(neworbit) and oldorbit - neworbit >= 0.15:
                    orbits = [oldorbit / 1.4] + orbits
                    # Because this worked we'll try to do this one more time
                    oldorbit = oldorbit / 1.4
                    allowed = True
        return orbits

    def make_content_list(self):
        """
        Initialize orbit content dictionary

        Make a dictionary: Orbit: Content. Initially this will only contain the
        first gas giant. (If gas giant arrangement is not "None")
        """

        self.__orbitcontents = dict.fromkeys(self.__orbitarray)

        # Put the first gas giant
        if self.__gasarrangement is not 'None':
            # Check whether roll bonus for size is applicable here
            bonus = self.gas_giant_bonus(self.__firstgasorbit)

            # Add a GasGiant to the dict
            self.__orbitcontents[self.__firstgasorbit] = GasGiant(
                self.parentstar, self.__firstgasorbit, bonus)

    def place_gas_giants(self):
        """
        Populate orbit content dictionary with gas giants

        Iterate through all empty orbits and decide whether to place a gas
        giant there. Also check whether the orbit is eligible for a bonus.
        """

        rollorbits = [orb for orb in self.__orbitarray if self.__orbitcontents[orb] is None]
        small_orbits = [orb for orb in rollorbits if orb < self.__snowline]
        large_orbits = [orb for orb in rollorbits if orb > self.__snowline]
        if self.__gasarrangement is 'Epistellar':
            for stellar_orbit in small_orbits:
                if self.roller.roll_dice(3, 0) <= 6:
                    self.__orbitcontents[stellar_orbit] = GasGiant(self.parentstar,
                                                                   stellar_orbit, True)
            for stellar_orbit in large_orbits:
                if self.roller.roll_dice(3, 0) <= 14:
                    self.__orbitcontents[stellar_orbit] = GasGiant(self.parentstar,
                                                                   stellar_orbit, self.gas_giant_bonus(stellar_orbit))
        elif self.__gasarrangement is 'Eccentric':
            for stellar_orbit in small_orbits:
                if self.roller.roll_dice(3, 0) <= 8:
                    self.__orbitcontents[stellar_orbit] = GasGiant(self.parentstar,
                                                                   stellar_orbit, True)
            for stellar_orbit in large_orbits:
                if self.roller.roll_dice(3, 0) <= 14:
                    self.__orbitcontents[stellar_orbit] = GasGiant(self.parentstar,
                                                                   stellar_orbit, self.gas_giant_bonus(stellar_orbit))
        elif self.__gasarrangement is 'Conventional':
            for stellar_orbit in large_orbits:
                if self.roller.roll_dice(3, 0) <= 15:
                    self.__orbitcontents[stellar_orbit] = GasGiant(self.parentstar,
                                                                   stellar_orbit, self.gas_giant_bonus(stellar_orbit))

    def gas_giant_bonus(self, orbit):
        bonus = orbit <= self.__snowline
        if not bonus:
            gg_index = self.__orbitarray.index(orbit)
            if gg_index > 0:
                bonus = self.__orbitarray[gg_index - 1] < self.__snowline
        return bonus

    def fill_orbits(self):
        """
        Fill empty orbits with non-jovian entities (worlds and asteroid belts)
        """

        # Determine eligible orbits to roll for
        roll_orbits = [orb for orb in self.__orbitarray if self.__orbitcontents[orb] is None]
        roll_orbits.sort()
        # Go through these orbits and determine the contents
        for orbit in roll_orbits:
            roll_mod = self.orbit_fill_modifier(self.__orbitarray.index(orbit))
            dice_roll = self.roller.roll_dice(3, roll_mod)
            if 4 <= dice_roll <= 6:
                obj = AsteroidBelt(self.parentstar, orbit)
            if 7 <= dice_roll <= 8:
                obj = Planet(self.parentstar, orbit, "Tiny")
            if 9 <= dice_roll <= 11:
                obj = Planet(self.parentstar, orbit, "Small")
            if 12 <= dice_roll <= 15:
                obj = Planet(self.parentstar, orbit, "Standard")
            if dice_roll >= 16:
                obj = Planet(self.parentstar, orbit, "Large")
            if not dice_roll <= 3:
                self.__orbitcontents[orbit] = obj
        # Now remove all orbits that still have None as content
        orc = {k: v for k, v in self.__orbitcontents.items() if v is not None}
        self.__orbitcontents = orc

    def name_contents(self):
        counter = 0
        for key in sorted(self.__orbitcontents):
            counter += 1
            name = '{}-{}'.format(self.parentstar.get_letter(), counter)
            self.__orbitcontents[key].set_name(name)
            self.__orbitcontents[key].set_number(counter)

    def orbit_fill_modifier(self, orbitindex):
        modifier = 0
        orbits = self.__orbitarray
        # If the orbit is adjacent to a forbidden zone
        if self.__forbidden:
            if orbitindex == 0 and self.__outerforbidden < orbits[orbitindex]:
                modifier -= 6
            if orbitindex == len(orbits) - 1 and self.__innerforbidden > orbits[orbitindex]:
                modifier -= 6

        # If the orbit is adjacent to the inner or outer limit
        if orbitindex == 0 or orbitindex == len(orbits) - 1:
            modifier -= 3

        # If the next orbit outward is occupied by a gas giant
        if orbitindex is not len(orbits) - 1:
            if self.__orbitcontents[orbits[orbitindex + 1]] is not None:
                if self.__orbitcontents[orbits[orbitindex + 1]].type() is "Gas Giant":
                    modifier -= 6

        # If the next orbit inward is occupied by a gas giant
        if orbitindex is not 0:
            if self.__orbitcontents[orbits[orbitindex - 1]] is not None:
                if self.__orbitcontents[orbits[orbitindex - 1]].type() is "Gas Giant":
                    modifier -= 3

        return modifier

    def make_eccentricities(self):
        for k, oc in self.__orbitcontents.items():
            if self.__gasarrangement == 'Conventional':
                bonus = -6
            elif k == list(self.__orbitcontents)[0] \
                    and self.__gasarrangement == 'Epistellar' and oc.type() == 'Gas Giant':
                bonus = -6
            elif self.__gasarrangement == 'Eccentric' and oc.type() == 'Gas Giant' and k < self.__snowline:
                bonus = +4
            else:
                bonus = 0
            oc.eccentricity = oc.make_eccentricity(self.roller.roll_dice(3, bonus))
            oc.min_max = oc.make_min_max()

    def has_garden(self):
        ret = False
        for k, p in self.__orbitcontents.items():
            if p.type() == 'Terrestrial' and p.get_type() == 'Garden':
                ret = True
        return ret
