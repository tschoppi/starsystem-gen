import cherrypy
import os
import random as r
import sys

import operator

from gurpsspace import starsystem as starsys
from namegenerator import namegenerator
from cherrypy.lib.static import serve_file

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('webgui/templates'))


class WebServer(object):

    random_seed = None

    def set_seed(self, seed=None):
        if seed is None:
            seed = r.randint(1, sys.maxsize)
        self.random_seed = int(seed)

    @cherrypy.expose
    def index(self):
        # List the available naming schemes
        naming_schemes = []
        for scheme in namegenerator.NameGenerator().list_available_corpuses():
            naming_schemes.append(scheme)

        tmpl = env.get_template('index.html')
        return tmpl.render(naming_schemes=naming_schemes)

    @cherrypy.expose
    def starsystem(self, must_have_garden="False", open_cluster=None, num_stars=0, age=None, naming="", use_chain=False, depth=1, seed=None):

        input_seed = None if seed == '' or None else seed  # Correctly interpret "no input"
        self.set_seed(input_seed)  # reseed the PRNG, so that there is a unique seed every time
        r.seed(self.random_seed)

        if num_stars == "":
            num_stars = None
        elif int(num_stars) < 1 or int(num_stars) > 3:
            num_stars = None
        else:
            num_stars = int(num_stars)

        if naming != "":  # A naming scheme has been selected that is not the simple "A-1", "B-1" scheme.
            namegen = namegenerator.NameGenerator(int(depth), self.random_seed)
            namegen.read_file(naming)
            namegen.use_chain = use_chain
            cherrypy.session['namegen'] = namegen
        else:
            cherrypy.session['namegen'] = None

        arguments = {
            'open_cluster': open_cluster == "True",
            'num_stars': num_stars,
            'age': age
        }

        # Generate star systems until one is made that contains a Garden world if it's required.
        if must_have_garden == "True":
            garden = False
            while garden is not True:
                mysys = starsys.StarSystem(**arguments)
                garden = mysys.has_garden()
        else:
            mysys = starsys.StarSystem(**arguments)

        for star in mysys.stars:
            for key, v in star.planetsystem.get_orbitcontents().items():
                if namegen is not None:
                    simple_name = v.get_name().replace("-", "")
                    if cherrypy.session.get('name_of_' + simple_name) is None:
                        name = namegen.get_random_name()
                        star.planetsystem.get_orbitcontents()[key].set_name(name)
                        # For some reason, using simple_name here leads to storing stuff improperly and
                        # generating new names every time. No idea why.
                        cherrypy.session['name_of_' + v.get_name().replace("-", "")] = name
                    else:
                        name = cherrypy.session.get('name_of_' + simple_name)
                        star.planetsystem.get_orbitcontents()[key].set_name(name)

        cherrypy.session.save()

        tmpl = env.get_template('overview.html')
        cherrypy.session['starsystem'] = mysys
        cherrypy.response.cookie['names'] = {}
        return tmpl.render(starsystem=mysys, seed=self.random_seed)

    @cherrypy.expose
    def planetsystem(self, star_id=""):
        starsystem = cherrypy.session.get('starsystem')
        if starsystem is None:
            raise cherrypy.HTTPRedirect('/', 307)
        if star_id == "":
            raise cherrypy.HTTPRedirect('/', 307)
        else:
            star_id = int(star_id)

        tmpl = env.get_template('planetsystem.html')
        env.globals['translate_row'] = self.translate_row

        t_count = 0
        a_count = 0
        g_count = 0
        for key, _ in starsystem.stars[star_id].planetsystem.get_orbitcontents().items():
                if starsystem.stars[star_id].planetsystem.get_orbitcontents()[key].type() == 'Terrestrial':
                    t_count += 1
                if starsystem.stars[star_id].planetsystem.get_orbitcontents()[key].type() == 'Ast. Belt':
                    a_count += 1
                if starsystem.stars[star_id].planetsystem.get_orbitcontents()[key].type() == 'Gas Giant':
                    g_count += 1

        cherrypy.session['planetsystem'] = starsystem.stars[star_id].planetsystem
        return tmpl.render(planetsystem=starsystem.stars[star_id].planetsystem, terrestrial_count=t_count, asteroid_count=a_count, gas_giant_count=g_count)

    @cherrypy.expose
    def satellites(self, planet_id=""):
        planetsystem = cherrypy.session.get('planetsystem')
        if planetsystem is None:
            raise cherrypy.HTTPRedirect('/', 307)
        if planet_id == "":
            raise cherrypy.HTTPRedirect('/', 307)
        else:
            planet_id = float(planet_id)

        planet = planetsystem.get_orbitcontents()[planet_id]
        if planet.type() == 'Terrestrial':
            moons = planet.get_satellites()
        else:
            moons = planet.get_moons()

        for moon in moons:
            if len(moon.get_name().split('-')) == 3:
                index = moon.get_name().split('-')[2]
                moon.set_name(planet.get_name() + '-' + index)

        cherrypy.session['moons'] = moons

        tmpl = env.get_template('moons.html')
        return tmpl.render(moons=moons, planet_name=planet.get_name())

    @cherrypy.expose
    def printable(self):
        try:
            starsystem = cherrypy.session['starsystem']
        except KeyError:
            raise cherrypy.HTTPError(404)

        t_count = 0
        a_count = 0
        g_count = 0
        for star in starsystem.stars:
            for key, _ in star.planetsystem.get_orbitcontents().items():
                if star.planetsystem.get_orbitcontents()[key].type() == 'Terrestrial':
                    t_count += 1
                if star.planetsystem.get_orbitcontents()[key].type() == 'Ast. Belt':
                    a_count += 1
                if star.planetsystem.get_orbitcontents()[key].type() == 'Gas Giant':
                    g_count += 1

        tmpl = env.get_template('printable.html')
        env.globals['translate_row'] = self.translate_row

        return tmpl.render(starsystem=starsystem, seed=self.random_seed, terrestrial_count=t_count, asteroid_count=a_count, gas_giant_count=g_count)

    def translate_row(self, planet, row):
        """
        It is difficult in HTML and Jinja to make a table where each column is a single item, rather than each row.
        This function helps out by returning the appropriate data for each row.
        :param planet: The orbital body to be queried.
        :param row: The row which determines the query.
        :return: The  data appropriate to the given row.
        """
        if row == '':
            return planet.get_name()
        if row == 'World Size':
            return planet.get_size()
        if row == 'World Type':
            return planet.get_type()
        if row == 'Atm. Mass*':
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
        if row == 'Density*':
            return planet.get_density()
        if row == 'Diameter*':
            return round(planet.get_diameter(), 2)
        if row == 'Surface Gravity':
            return round(planet.get_gravity(), 2)
        if row == 'Mass*':
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
        if row == 'Rotational Period*':
            retval = str(round(planet.get_rotation(), 2))
            retval += " days"
            return retval
        if row == 'Blackbody Temperature':
            return str(round(planet.get_blackbody_temp(), 2)) + ' K'
        if row == 'Cloudtop Gravity':
            return round(planet.get_gravity(), 2)
        else:
            return 'Not implemented yet'

if __name__ == '__main__':

    # Configure CherryPy with a Python dictionary for Python 3.5 compatibility.
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8000
        },
        '/': {
            'tools.sessions.on': True,
            'tools.sessions.timeout': 60,
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "webgui/static",
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/favicon': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.abspath(os.getcwd()) + "/webgui/static/favicon.ico"
        },
        '/scripts': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "webgui/scripts"
        }
    }
    cherrypy.quickstart(WebServer(), '/', conf)
