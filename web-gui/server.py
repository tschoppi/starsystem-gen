import cherrypy

import os
import sys

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

        return tmpl.render(starsystem=mysys)

if __name__ == '__main__':
    # This line reads the global server config from the file
    cherrypy.config.update("server.conf")
    # The third argument reads the application config from the file.
    # This is necessary, because apparently the route mapping is application-specific.
    cherrypy.quickstart(WebServer(), '/', "server.conf")
