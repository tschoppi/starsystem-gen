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
    def starsystem(self, must_have_garden="False", open_cluster=None, num_stars=0, age=None):
        if num_stars == "":
            num_stars = None
        elif int(num_stars) < 1 or int(num_stars) > 3:
            num_stars = None
        else:
            num_stars = int(num_stars)

        args = {
            'open_cluster': open_cluster == "True",
            'num_stars': num_stars,
            'age': age
        }

        # Generate starsystems until one is made that contains a Garden world if it's required.
        if must_have_garden == "True":
            garden = False
            cyclenum = 0
            while garden is not True:
                cyclenum += 1
                mysys = starsys.StarSystem(**args)
                garden = mysys.has_garden()
        else:
            mysys = starsys.StarSystem(**args)

        tmpl = env.get_template('overview.html')
        cherrypy.session['starsystem'] = mysys
        return tmpl.render(starsystem=mysys)

    @cherrypy.expose
    def planetsystem(self, star_id=""):
        starsystem = cherrypy.session.get('starsystem')
        if starsystem is None:
            raise cherrypy.HTTPRedirect('/index.html', 307)
        if star_id == "":
            raise cherrypy.HTTPRedirect('/index.html', 307)
        else:
            star_id = int(star_id)

        tmpl = env.get_template('planetsystem.html')
        env.globals['translate_row'] = self.translate_row
        count = 0
        for key, _ in starsystem.stars[star_id].planetsystem.get_orbitcontents().items():
                if starsystem.stars[star_id].planetsystem.get_orbitcontents()[key].type() == 'Terrestrial':
                    count += 1
        tcount = count
        count = 0
        for key, _ in starsystem.stars[star_id].planetsystem.get_orbitcontents().items():
                if starsystem.stars[star_id].planetsystem.get_orbitcontents()[key].type() == 'Ast. Belt':
                    count += 1
        acount = count
        cherrypy.session['planetsystem'] = starsystem.stars[star_id].planetsystem
        return tmpl.render(planetsystem=starsystem.stars[star_id].planetsystem, terrestrial_count=tcount, asteroid_count=acount)

    def translate_row(self, key, row):
        planetsystem = cherrypy.session.get('planetsystem')
        planet = planetsystem.get_orbitcontents()[key]
        if row == '':
            return planet.get_name().replace("<", "").replace(">", "")
        if row == 'World Size':
            return planet.get_size()
        if row == 'World Type':
            return planet.get_type()
        if row == 'Atm. Mass':
            return str(planet.get_atmospheric_mass())
        if row == 'Atm. Composition' and planet.get_atmospheric_mass() > 0:
            retval = ''
            atmospheric_components = sorted(planet.atmcomp.items(), key=operator.itemgetter(0))
            for name, present in atmospheric_components:
                if present:
                    retval += name + '<br/>'
            if len(retval) == 0:
                retval = 'Breathable'
            return retval
        elif row == 'Atm. Composition' and planet.get_atmospheric_mass() == 0:
            return 'Trace or No Atmosphere'
        if row == 'Hydr. Coverage':
            return str(round(planet.get_hydrographic_cover(), 2)) + ' %'
        if row == 'Avg. Surface Temperature':
            return str(round(planet.get_average_surface_temp(), 2)) + ' K / ' + str(round(planet.get_average_surface_temp() - 273.15, 2)) + '°C'
        if row == 'Climate Type':
            return planet.get_climate()
        if row == 'Axial Tilt':
            return str(planet.get_axial_tilt()) + '°'
        if row == 'Density':
            return planet.get_density()
        if row == 'Diameter':
            return round(planet.get_diameter(), 2)
        if row == 'Surface Gravity':
            return round(planet.get_gravity(), 2)
        if row == 'Mass':
            return round(planet.get_mass(), 2)
        if row == 'Atm. Pressure':
            return str(round(planet.get_pressure(), 2)) + ' atm'
        if row == 'Pressure Category':
            return planet.get_pressure_category()
        if row == 'Total Tidal Effect':
            return round(planet.get_total_tidal_effect(), 2)
        if row == 'Volcanics':
            return planet.get_volcanism()
        if row == 'Tectonics':
            return planet.get_tectonics()
        if row == 'Resource Value Modifier':
            return planet.get_rvm()
        if row == 'Habitability':
            return planet.get_habitability()
        if row == 'Affinity':
            return planet.get_affinity()
        if row == 'Rotational Period':
            retval = str(round(planet.get_rotation(), 2))
            retval += " days"
            if planet.get_rotation() < 0:
                retval += " *"
            return retval
        else:
            return 'Not implemented yet'

if __name__ == '__main__':
    # This line reads the global server config from the file
    cherrypy.config.update("server.conf")
    # The third argument reads the application config from the file.
    # This is necessary, because apparently the route mapping is application-specific.
    cherrypy.quickstart(WebServer(), '/', "server.conf")
