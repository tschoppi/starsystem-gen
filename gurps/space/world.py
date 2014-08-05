from .orbitcontents import OrbitContent
from .tables import MAtmoTable, TempFactor, WorldClimate
from .tables import SizeConstrTable, PressureCategory
from math import floor

class World(OrbitContent):
    def __init__(self, primary, orbitalradius, sizeclass):
        OrbitContent.__init__(self, primary, orbitalradius)
        self.__sizeclass = sizeclass
        self.maketype()
        self.makeatmosphere()
        self.makehydrographics()
        self.makeclimate()
        self.makedensity()
        self.makediameter()
        self.makegravity()
        self.makemass()
        self.makepressure()

    def __repr__(self):
        return repr("World")

    def type(self):
        return "World"

    def getSize(self):
        return self.__sizeclass

    def maketype(self):
        bbtemp = self.getBBTemp()
        size = self.getSize()
        primmass = self.primarystar.getMass()
        type = 'Ice'
        if size == 'Tiny' and bbtemp >= 141:
            type = 'Rock'
        if size == 'Small':
            if bbtemp <= 80:
                type = 'Hadean'
            if bbtemp >= 141:
                type = 'Rock'
        if size == 'Standard':
            if bbtemp <= 80:
                type = 'Hadean'
        if size == 'Standard' or size == 'Large':
            if bbtemp > 150 and bbtemp <= 230 and primmass <= 0.65:
                type = 'Ammonia'
            if bbtemp > 240 and bbtemp <= 320:
                age = self.primarystar.getAge()
                if size == 'Standard':
                    cap = 10
                if size == 'Large':
                    cap = 5
                bonus = floor(age / 0.5)
                if bonus > cap:
                    bonus = cap
                dice = self.roll(3, bonus)
                if dice >= 18:
                    type = 'Garden'
                else:
                    type = 'Ocean'
            if bbtemp > 320 and bbtemp <= 500:
                type = 'Greenhouse'
            if bbtemp > 500:
                type = 'Chthonian'
        self.__type = type

    def getType(self):
        return self.__type

    def getAtmass(self):
        return self.__atmmass

    def makeatmosphere(self):
        size = self.getSize()
        type = self.getType()
        # Determine atmospheric mass
        if size == 'Tiny' or type == 'Hadean' or type == 'Chthonian' or  type == 'Rock':
            self.__atmmass = 0
        else:
            self.__atmmass = self.roll(3,0) / 10.

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
            if self.roll(3,0) > 15:
                self.atmcomp['Lethally Toxic'] = True
            else:
                self.atmcomp['Mildly Toxic'] = True

        if type == 'Ammonia' or type == 'Greenhouse':
            self.atmcomp['Suffocating'] = True
            self.atmcomp['Lethally Toxic'] = True
            self.atmcomp['Corrosive'] = True

        if type == 'Garden':
            if self.roll(3,0) >= 12:
                self.__hasmarginal = True
                self.__marginal = MAtmoTable[self.roll(3,0)]

        if size == 'Standard' and (type == 'Ice' or type == 'Ocean'):
            self.atmcomp['Suffocating'] = True
            if self.roll(3,0) > 12:
                self.atmcomp['Mildly Toxic'] = True

        if size == 'Large' and (type == 'Ice' or type == 'Ocean'):
            self.atmcomp['Highly Toxic'] = True
            self.atmcomp['Suffocating'] = True

    def getMarginal(self):
        """Return a tuple:
        (boolean: marginal, marginal atmosphere)
        """
        return (self.__hasmarginal, self.__marginal)

    def makehydrographics(self):
        hydro = 0
        size = self.getSize()
        type = self.getType()
        if size == 'Small' and type == 'Ice':
            hydro = self.roll(1,2) * 10
        if type == 'Ammonia':
            hydro = self.roll(2,0) * 10
            if hydro > 100:
                hydro = 100
        if type == 'Ice' and (size == 'Standard' or size == 'Large'):
            hydro = self.roll(2,-10) * 10
            if hydro < 0:
                hydro = 0
        if type == 'Ocean' or type == 'Garden':
            bonus = 4
            if size == 'Large':
                bonus = 6
            hydro = self.roll(1, bonus) * 10
            if hydro > 100:
                hydro = 100
        if type == 'Greenhouse':
            hydro = self.roll(2, -7) * 10
            if hydro < 0:
                hydro = 0
        self.__hydrocover = hydro

    def getHydrocover(self):
        return self.__hydrocover

    def absorptiongreenhouse(self):
        """
        Return a tuple (absorption factor, greenhouse factor) based on world
        type and size.
        """
        type = self.getType()
        size = self.getSize()
        if type is not 'Garden' and type is not 'Ocean':
            return TempFactor[type][size]
        else:
            hydro = self.getHydrocover()
            abs = 0.84
            if hydro <= 90:
                abs = 0.88
            if hydro <= 50:
                abs = 0.92
            if hydro <= 20:
                abs = 0.95
            return (abs, 0.16)

    def makeclimate(self):
        abs, green = self.absorptiongreenhouse()
        matm  = self.getAtmass()
        bbcorr = abs * (1 + (matm * green))
        self.__averagesurface = bbcorr * self.getBBTemp()
        self.__climatetype = WorldClimate(self.__averagesurface)

    def getAvSurf(self):
        return self.__averagesurface

    def getClimate(self):
        return self.__climatetype

    def makedensity(self):
        type = self.getType()
        size = self.getSize()
        density = 0
        dice = self.roll(3,0)
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
        self.__density = density

    def getDensity(self):
        return self.__density

    def makediameter(self):
        size = self.getSize()
        bb = self.getBBTemp()
        dens = self.getDensity()
        smin, smax = SizeConstrTable[size]
        term = (bb / dens) ** (0.5)
        min = term * smin
        max = term * smax
        diff = max - min
        diam = self.roll(2, -2) * 0.1 * diff + min
        self.__diameter = diam

    def getDiameter(self):
        return self.__diameter

    def makegravity(self):
        self.__surfacegravity = self.getDensity() * self.getDiameter()

    def getGravity(self):
        return self.__surfacegravity

    def makemass(self):
        self.__mass = self.getDensity() * self.getDiameter() ** 3

    def getMass(self):
        return self.__mass

    def makepressure(self):
        size = self.getSize()
        type = self.getType()
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
            pressure = self.getMass() * factor * self.getGravity()
            category = PressureCategory(pressure)
        self.__pressure = pressure
        self.__presscat = category

    def getPressure(self):
        return self.__pressure

    def getPressCat(self):
        return self.__presscat

    def makevolcanism(self):
        bonus = self.getGravity() / self.primarystar.getAge()
        bonus += self.volcanicbonus()
        volcanoroll = self.roll(3, bonus)
        activity = 'None'
        if volcanoroll > 16:
            activity = 'Light'
        if volcanoroll > 20:
            activity = 'Moderate'
        if volcanoroll > 26:
            activity = 'Heavy'
        if volcanoroll > 70:
            activity = 'Extreme'
        self.__volcanism = activity

    def getVolcanism(self):
        return self.__volcanism

    def volcanicbonus(self):
        return 0

    def maketectonism(self):
        if self.getSize() == 'Small' or self.getSize() == 'Tiny':
            self.__tectonic = 'None'
        else:
            volc = self.getVolcanism()
            bonus = 0
            if volc == 'None':
                bonus -= 8
            if volc == 'Light':
                bonus -= 4
            if volc == 'Heavy':
                bonus += 4
            if volc == 'Extreme':
                bonus += 8
            if self.getHydrocover() < 50:
                bonus -= 2
            bonus += self.tectonicbonus()
            tect = self.roll(3, bonus)
            activity = 'None'
            if tect > 6:
                activity = 'Light'
            if tect > 10:
                activity = 'Moderate'
            if tect > 14:
                activity = 'Heavy'
            if tect > 18:
                activity = 'Extreme'
            self.__tectonic = activity

    def tectonicbonus(self):
        return 0

    def getTectonics(self):
        return self.__tectonic

    def resourcebonus(self):
        volc = self.getVolcanism()
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

    def makeresources(self):
        rollbonus = self.resourcebonus()
        dice = self.roll(3, rollbonus)
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
        if dice> 18:
            rvm = 3
            value = 'Rich'
        self.__rvm = rvm
        self.__resources = value

    def getRVM(self):
        return self.__rvm

    def getResources(self):
        return self.__resources

    def makehabitability(self):
        modifier = 0
        # The following is from p. 121
        volc = self.getVolcanism()
        tect = self.getTectonics()
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
            press = self.getPressCat()
            if press == 'Very Thin':
                modifier += 1
            if press == 'Thin':
                modifier += 2
            if press == 'Standard' or press == 'Dense':
                modifier += 3
            if press == 'Very Dense' or press == 'Superdense':
                modifier += 1
            hasmarg, marg = self.getMarginal()
            if not hasmarg:
                modifier += 1
            climate = self.getClimate()
            if climate == 'Cold' or climate == 'Hot':
                modifier += 1
            if climate in ['Chilly', 'Cool', 'Normal', 'Warm', 'Tropical']:
                modifier += 2
        # Now the Hydrographics Coverage conditions
        if self.getType() in ['Garden', 'Ocean']:
            hydro = self.getHydrocover()
            if (hydro > 0 and hydro < 60) or (hydro > 90 and hydro < 100):
                modifier += 1
            elif hydro > 0:
                modifier += 2

        # Check lower bounds (p. 121)
        if modifier < -2:
            modifier = -2
        self.__habitability = modifier

    def getHabitability(self):
        return self.__habitability

    def makeaffinity(self):
        self.__affinity = self.getRVM() + self.getHabitability()

    def getAffinity(self):
        return self.__affinity
