import cherrypy

import os
import sys
import operator

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

# This adds '..' to the search path for python,
# so that ../gurpsspace can be imported
# TODO: Fix Modules so this is no longer necessary,
# most likely by creating a top-level module
# Then from .. import gurpsspace should work
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(path)
if path not in sys.path:
    sys.path.insert(1, path)
del path

# This import is not at the top of the file, due to aforementioned path issues
from gurpsspace import starsystem as starsys


class WebServer(object):

    @cherrypy.expose
    def starsystem(self, must_have_garden="False", opencluster=None, numstars=0, age=None):
        if numstars == "":
            numstars = None
        elif int(numstars) < 1 or int(numstars) > 3:
            numstars = None
        else:
            numstars = int(numstars)

        args = {
            'opencluster': opencluster == "True",
            'numstars': numstars,
            'age': age
        }

        # Generate starsystems until one is made that contains a Garden world if it's required.
        if must_have_garden == "True":
            garden = False
            cyclenum = 0
            while garden is not True:
                cyclenum += 1
                mysys = starsys.StarSystem(**args)
                garden = mysys.hasgarden()
        else:
            mysys = starsys.StarSystem(**args)

        tmpl = env.get_template('overview.html')
        cherrypy.session['starsystem'] = mysys
        return tmpl.render(starsystem=mysys)

    @cherrypy.expose
    def planetsystem(self, star_id):
        starsystem = cherrypy.session.get('starsystem')
        if starsystem is None:
            raise cherrypy.HTTPError(500, "No star system was in the session store!")
        if star_id == "":
            raise cherrypy.HTTPError(500, "There was no star selected!")
        else:
            star_id = int(star_id)

        tmpl = env.get_template('planetsystem.html')
        env.globals['translate_row'] = self.translate_row
        count = 0
        for key, _ in starsystem.stars[star_id].planetsystem.getOrbitcontents().items():
                if starsystem.stars[star_id].planetsystem.getOrbitcontents()[key].type() == 'Terrestrial':
                    count += 1
        tcount = count
        count = 0
        for key, _ in starsystem.stars[star_id].planetsystem.getOrbitcontents().items():
                if starsystem.stars[star_id].planetsystem.getOrbitcontents()[key].type() == 'Ast. Belt':
                    count += 1
        acount = count
        cherrypy.session['planetsystem'] = starsystem.stars[star_id].planetsystem
        return tmpl.render(planetsystem=starsystem.stars[star_id].planetsystem, terrestrial_count=tcount, asteroid_count=acount)

    def translate_row(self, key, row):
        planetsystem = cherrypy.session.get('planetsystem')
        planet = planetsystem.getOrbitcontents()[key]
        if row == '':
            return planet.getName().replace("<", "").replace(">", "")
        if row == 'World Size':
            return planet.getSize()
        if row == 'World Type':
            return planet.getType()
        if row == 'Atm. Mass':
            return str(planet.getAtmass())
        if row == 'Atm. Composition' and planet.getAtmass() > 0:
            retval = ''
            atmospheric_components = sorted(planet.atmcomp.items(), key=operator.itemgetter(0))
            for name, present in atmospheric_components:
                if present:
                    retval += name + '<br/>'
            if len(retval) == 0:
                retval = 'Breathable'
            return retval
        elif row == 'Atm. Composition' and planet.getAtmass() == 0:
            return 'Trace or No Atmosphere'
        if row == 'Hydr. Coverage':
            return str(round(planet.getHydrocover(), 2)) + ' %'
        if row == 'Avg. Surface Temperature':
            return str(round(planet.getAvSurf(), 2)) + ' K / ' + str(round(planet.getAvSurf() - 273.15, 2)) + '°C'
        if row == 'Climate Type':
            return planet.getClimate()
        if row == 'Axial Tilt':
            return str(planet.getAxialTilt()) + '°'
        if row == 'Density':
            return planet.getDensity()
        if row == 'Diameter':
            return round(planet.getDiameter(), 2)
        if row == 'Surface Gravity':
            return round(planet.getGravity(), 2)
        if row == 'Mass':
            return round(planet.getMass(), 2)
        if row == 'Atm. Pressure':
            return round(planet.getPressure(), 2)
        if row == 'Pressure Category':
            return planet.getPressCat()
        if row == 'Total Tidal Effect':
            return round(planet.getTTE(), 2)
        if row == 'Volcanics':
            return planet.getVolcanism()
        if row == 'Tectonics':
            return planet.getTectonics()
        if row == 'Resource Value Modifier':
            return planet.getRVM()
        if row == 'Habitability':
            return planet.getHabitability()
        if row == 'Affinity':
            return planet.getAffinity()
        if row == 'Rotational Period':
            return round(planet.getRotation(), 2)
        else:
            return 'Not implemented yet'

if __name__ == '__main__':
    # This line reads the global server config from the file
    cherrypy.config.update("server.conf")
    # The third argument reads the application config from the file.
    # This is necessary, because apparently the route mapping is application-specific.
    cherrypy.quickstart(WebServer(), '/', "server.conf")
