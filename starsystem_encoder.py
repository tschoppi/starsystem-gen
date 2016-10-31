import json
import cherrypy


from json import JSONEncoder


class StarsystemEncoder(JSONEncoder):

    def default(self, *args, **kwargs):
        to_encode = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
        return self.encode_starsystem(to_encode)

    def encode_starsystem(self, current_system):

        jsonable = dict()

        jsonable["seed"] = current_system.seed
        jsonable["age"] = current_system.age
        jsonable["open_cluster"] = current_system.opencluster

        if len(current_system.stars) > 1:
            jsonable["orbits"] = current_system.orbits
            jsonable["periods"] = current_system.periods

        stars = []
        for i in range(len(current_system.stars)):
            stars.append(self.encode_star(current_system.stars[i]))

        jsonable["stars"] = stars

        return json.dumps(jsonable).encode('utf8')

    def encode_star(self, star):

        jsonable = dict()

        jsonable["letter"] = star.get_letter()

        jsonable["mass"] = star.get_mass()
        jsonable["sequence"] = star.get_sequence()
        jsonable["luminosity"] = star.get_luminosity()
        jsonable["temperature"] = star.get_temp()
        jsonable["radius"] = round(star.get_radius(), 6)
        jsonable["orbital_limits"] = star.get_orbit_limits()
        jsonable["snowline"] = star.get_snowline()
        if star.has_forbidden_zone():
            # Nicely formatted forbidden zone
            jsonable["forbidden_zone"] = star.get_forbidden_zone()
        else:
            jsonable["forbidden_zone"] = ""

        if len(star.planetsystem.get_orbitcontents()) > 0:
            jsonable["planets"] = self.encode_planets(star.planetsystem.get_orbitcontents())
        else:
            jsonable["planets"] = []

        return jsonable

    def encode_planets(self, planets):
        jsonable = list()

        for key, planet in planets.items():
            dictified = dict()
            dictified["name"] = planet.get_name()
            dictified["type"] = planet.type()
            dictified["size"] = planet.get_size()
            dictified["world_type"] = planet.get_type()
            dictified["orbital_radius"] = planet.get_orbit()
            dictified["orbital_period"] = planet.get_period()
            dictified["eccentricity"] = planet.get_eccentricity()
            dictified["min_max_orbit"] = planet.get_min_max()
            if planet.num_moons() > 0:
                dictified["moons"] = self.encode_moons(planet)
            else:
                dictified["moons"] = []
            dictified["moonlets"] = planet.num_moonlets()
            jsonable.append(dictified)

        return jsonable
