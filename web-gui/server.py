import cherrypy
import mimetypes

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
    def generate(self, mustHaveGarden=False):
        return "<h1>Hello world!</h1> <br/>" + str(mustHaveGarden)

if __name__ == '__main__':
   ## This line reads the global server config from the file
   cherrypy.config.update("server.conf")
   ## The third argument reads the application config from the file.
   ## This is necessary, because apparently the route mapping is application-specific.
   cherrypy.quickstart(WebServer(), '/', "server.conf")
