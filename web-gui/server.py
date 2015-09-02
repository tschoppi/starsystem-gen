import cherrypy, mimetypes
import os, sys, json

## This adds '..' to the search path for python, so that ../gurpsspace can be imported
## TODO: Fix Modules so this is no longer necessary, most likely by creating a top-level module
## Then from .. import gurpsspace should work
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print (path)
if not path in sys.path:
    sys.path.insert(1, path)
del path

from gurpsspace import starsystem as starsys

## mimetypes.types_map['.csv'] = 'text/csv'
## This sets a mimetype manually, in case mimetypes doesn't guess right


## [/style.css]
## tools.staticfile.on = True
## tools.staticfile.filename = "/home/site/style.css"
## This serves a  single static file MUST BE ABSOLUTE PATH!

## [/static]
## tools.staticdir.on = True
## tools.staticdir.dir = "/home/site/static"
## tools.staticdir.index = "index.html"
## This serves a directory MUST BE ABSOLUTE PATH! Windows?

 
class WebServer(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def generate(self, mustHaveGarden=False):
        # Change from None to a value if you want to set an argument
        args = {
            'opencluster': None, # True or False
            'numstars': None, # 1, 2 or 3
            'age': None # Number > 0
        }

        # Generate starsystems until one is made that contains a Garden world.
        if mustHaveGarden == "True":
            garden = False
            cyclenum = 0
            while garden is not True:
                cyclenum += 1
                mysys = starsys.StarSystem(**args)
                garden = mysys.hasgarden()
        else:
            mysys = starsys.StarSystem(**args)

        print (mysys.getinfo())
        return mysys.getinfo()

if __name__ == '__main__':
   ## This line reads the global server config from the file
   cherrypy.config.update("server.conf")
   ## The third argument reads the application config from the file.
   ## This is necessary, because apparently the route mapping is application-specific.
   cherrypy.quickstart(WebServer(), '/', "server.conf")
