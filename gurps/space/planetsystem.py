from . import dice as GD
from . import orbitcontents as OC
from .tables import OrbitalSpace

class PlanetSystem:
    def roll(self, dicenum, modifier):
        return self.roller.roll(dicenum, modifier)

    def __init__(self, parentstar):
        self.roller = GD.DiceRoller()
        self.parentstar = parentstar
        self.__innerlimit, self.__outerlimit = parentstar.getOrbitlimits()
        self.__snowline = parentstar.getSnowline()
        self.__primarylum = parentstar.getLuminosity()
        self.__forbidden = parentstar.hasForbidden()
        if self.__forbidden:
            self.__innerforbidden, self.__outerforbidden = parentstar.getForbidden()
        self.makegasgiantarrangement()
        self.placefirstgasgiant()
        self.createorbits()
        self.makecontentlist()
        self.placegasgiants()
        self.fillorbits()

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

    def printorbcontent(self):
        first = True
        for skey in sorted(self.__orbitcontents):
            if first:
                print("Orb Content:\t{}: {}".format(round(skey,3), self.__orbitcontents[skey]))
                first = False
            else:
                print("\t\t{}: {}".format(round(skey,3), self.__orbitcontents[skey]))

    def allowedorbit(self, testorbit):
        result  = testorbit >= self.__innerlimit
        result &= testorbit <= self.__outerlimit
        if self.__forbidden and result:
            result2 = testorbit <= self.__innerforbidden
            result2 |= testorbit >= self.__outerforbidden
            return result & result2
        else:
            return result

    def makegasgiantarrangement(self):
        dice = self.roll(3,0)
        self.__gasarrangement = 'None'
        if dice > 10:
            self.__gasarrangement = 'Conventional'
        if dice > 12:
            self.__gasarrangement = 'Eccentric'
        if dice > 14:
            self.__gasarrangement = 'Epistellar'

    def placefirstgasgiant(self):
        orbit = 0
        if self.__gasarrangement == 'Conventional':
            orbit = (1 + (self.roll(2,-2) * 0.05)) * self.__snowline
        if self.__gasarrangement == 'Eccentric':
            orbit = self.roll(1,0) * 0.125 * self.__snowline
        if self.__gasarrangement == 'Epistellar':
            orbit = self.roll(3,0) * 0.1 * self.__innerlimit
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
            orbitsout = self.orbitoutward(innermost)
            orbits += orbitsout
        elif self.__gasarrangement == 'Epistellar':
            # Create orbits outwards. Since the epistellar GasGiant is closer to
            # the star than the inner orbital limit, special conditions apply
            orbits += [self.__firstgasorbit]
            startorbit = self.__firstgasorbit + 0.15
            # If the minimal distance is not within the orbital zone make the
            # next orbit right at the border
            if not self.allowedorbit(startorbit):
                startorbit = self.__innerlimit
            orbits += [startorbit]
            orbitsout = self.orbitoutward(startorbit)
            orbits += orbitsout
        else:
            # Create orbits inwards then outwards from first gas giant
            orbits += [self.__firstgasorbit]
            orbitsin = self.orbitinward(self.__firstgasorbit)
            orbitsout = self.orbitoutward(self.__firstgasorbit)
            orbits = orbitsin + orbits
            orbits += orbitsout
        self.__orbitarray = orbits

    def orbitoutward(self, startorbit):
        allowed = True
        orbits = []
        oldorbit = startorbit
        neworbit = 0
        while(allowed):
            orbsep = OrbitalSpace[self.roll(3,0)]
            neworbit = oldorbit * orbsep
            if self.allowedorbit(neworbit) and neworbit - oldorbit >= 0.15:
                orbits += [neworbit]
                oldorbit = neworbit
            else:
                allowed = False
                neworbits = [oldorbit * 1.4, oldorbit * 2.0]
                success = False
                # Check 1.4 and 2.0 if allowed, take the first
                for neworb in neworbits:
                    if self.allowedorbit(neworb):
                        if neworb - oldorbit >= 0.15:
                            success = True
                            neworbit = neworb
                            oldorbit = neworb
                            break
                if success:
                    orbits += [neworbit]
                    allowed = True
                else:
                    # If our searching yielded nothing, check if there is an
                    # allowed orbit with the minimal distance, and put that
                    if self.allowedorbit(oldorbit + 0.15) and self.allowedorbit(oldorbit * 1.4):
                        neworbit = oldorbit + 0.15
                        orbits += [neworbit]
                        oldorbit = neworbit
                        allowed = True


        return orbits

    def orbitinward(self, startorbit):
        allowed = True
        orbits = []
        oldorbit = startorbit
        neworbit = 0
        while(allowed):
            orbsep = OrbitalSpace[self.roll(3,0)]
            neworbit = oldorbit / orbsep
            if self.allowedorbit(neworbit) and oldorbit - neworbit >= 0.15:
                orbits = [neworbit] + orbits
                oldorbit = neworbit
            else:
                allowed = False
                # Check to fit one last orbit
                neworbit = oldorbit / 1.4
                if self.allowedorbit(neworbit) and oldorbit - neworbit >= 0.15:
                    orbits = [oldorbit / 1.4] + orbits
                    # Because this worked we'll try to do this one more time
                    oldorbit = oldorbit / 1.4
                    allowed = True
        return orbits


    def makecontentlist(self):
        # Make a dictionary: Orbit: Content. Initially this will only contain
        # the first gas giant. (If gas giant arrangement is not "None")
        orbits = self.__orbitarray
        self.__orbitcontents = dict.fromkeys(self.__orbitarray)

        # Put the first gas giant
        if self.__gasarrangement is not 'None':
            # Check whether roll bonus for size is applicable here
            bonus = self.gasgiantbonus(self.__firstgasorbit)

            # Add a GasGiant to the dict
            self.__orbitcontents[self.__firstgasorbit] = OC.GasGiant(
                self.__primarylum, self.__firstgasorbit, self.__snowline, bonus)

    def placegasgiants(self):
        # Iterate through all orbits necessary and decide whether to place a
        # gas giant there. Also check whether the orbit is eligible for a bonus

        rollorbits = [orb for orb in self.__orbitarray if self.__orbitcontents[orb] is None]
        smallorbits = [orb for orb in rollorbits if orb < self.__snowline]
        largeorbits = [orb for orb in rollorbits if orb > self.__snowline]
        if self.__gasarrangement is 'Epistellar':
            for so in smallorbits:
                if self.roll(3,0) <= 6:
                    self.__orbitcontents[so] = OC.GasGiant(self.__primarylum,
                        so, self.__snowline, True)
            for so in largeorbits:
                if self.roll(3,0) <= 14:
                    self.__orbitcontents[so] = OC.GasGiant(self.__primarylum,
                        so, self.__snowline, self.gasgiantbonus(so))
        elif self.__gasarrangement is 'Eccentric':
            for so in smallorbits:
                if self.roll(3,0) <= 8:
                    self.__orbitcontents[so] = OC.GasGiant(self.__primarylum,
                        so, self.__snowline, True)
            for so in largeorbits:
                if self.roll(3,0) <= 14:
                    self.__orbitcontents[so] = OC.GasGiant(self.__primarylum,
                        so, self.__snowline, self.gasgiantbonus(so))
        elif self.__gasarrangement is 'Conventional':
            for so in largeorbits:
                if self.roll(3,0) <= 15:
                    self.__orbitcontents[so] = OC.GasGiant(self.__primarylum,
                        so, self.__snowline, self.gasgiantbonus(so))

    def gasgiantbonus(self, orbit):
        bonus = orbit <= self.__snowline
        if not bonus:
            ggindex = self.__orbitarray.index(orbit)
            if ggindex > 0:
                bonus = self.__orbitarray[ggindex-1] < self.__snowline
        return bonus

    def fillorbits(self):
        # Determine eligible orbits to roll for
        rollorbits = [orb for orb in self.__orbitarray if self.__orbitcontents[orb] is None]
        rollorbits.sort()
        # Go through these orbits and determine the contents
        for orbit in rollorbits:
            rollmod = self.orbitfillmodifier(self.__orbitarray.index(orbit))
            diceroll = self.roll(3, rollmod)
            if diceroll >= 4 and diceroll <= 6:
                obj = OC.AsteroidBelt(self.__primarylum, orbit)
            if diceroll >= 7 and diceroll <= 8:
                obj = OC.Planet(self.__primarylum, orbit, "Tiny")
            if diceroll >= 9 and diceroll <= 11:
                obj = OC.Planet(self.__primarylum, orbit, "Small")
            if diceroll >= 12 and diceroll <= 15:
                obj = OC.Planet(self.__primarylum, orbit, "Standard")
            if diceroll >= 16:
                obj = OC.Planet(self.__primarylum, orbit, "Large")
            if not diceroll <= 3:
                self.__orbitcontents[orbit] = obj


    def orbitfillmodifier(self, orbitindex):
        modifier = 0
        orbits = self.__orbitarray
        # If the orbit is adjacent to a forbidden zone
        if self.__forbidden:
            if orbitindex == 0 and self.__outerforbidden < orbits[orbitindex]:
                modifier -= 6
            if orbitindex == len(orbits)-1 and self.__innerforbidden > orbits[orbitindex]:
                modifier -= 6

        # If the orbit is adjacent to the inner or outer limit
        if orbitindex == 0 or orbitindex == len(orbits)-1:
            modifier -= 3

        # If the next orbit outward is occupied by a gas giant
        if orbitindex is not len(orbits)-1:
            if self.__orbitcontents[orbits[orbitindex + 1]] is not None:
                if self.__orbitcontents[orbits[orbitindex + 1]].type() is "Gas Giant":
                    modifier -= 6

        # If the next orbit inward is occupied by a gas giant
        if orbitindex is not 0:
            if self.__orbitcontents[orbits[orbitindex - 1]] is not None:
                if self.__orbitcontents[orbits[orbitindex - 1]].type() is "Gas Giant":
                    modifier -= 3

        return modifier
