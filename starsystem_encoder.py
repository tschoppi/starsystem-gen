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

            if planet.type() == "Terrestrial":
                dictified["atmospheric_mass"] = planet.get_atmospheric_mass()
                dictified["atmospheric_composition"] = planet.atmcomp
                dictified["atmospheric_pressure"] = planet.get_pressure()
                dictified["pressure_category"] = planet.get_pressure_category()
                dictified["hydrographic_coverage"] = planet.get_hydrographic_cover()
                dictified["volcanism"] = planet.get_volcanism()
                dictified["density"] = planet.get_density()
                dictified["diameter"] = planet.get_diameter()
                dictified["gravity"] = planet.get_gravity()
                dictified["mass"] = planet.get_mass()
                dictified["tectonics"] = planet.get_tectonics()
                dictified["resource_value_modifier"] = planet.get_rvm()
                dictified["habitability"] = planet.get_habitability()
                dictified["affinity"] = planet.get_affinity()
                dictified["rotational_period"] = planet.get_rotation()
                dictified["avg_surface_temperature"] = planet.get_average_surface_temp()
                dictified["climate"] = planet.get_climate()
                dictified["resource_value_modifier"] = planet.get_rvm()
                dictified["affinity"] = planet.get_affinity()
                dictified["axial_tilt"] = planet.get_axial_tilt()

            if planet.type() == "Ast. Belt":
                dictified["avg_surface_temperature"] = planet.get_average_surface_temp()
                dictified["climate"] = planet.get_climate()
                dictified["resource_value_modifier"] = planet.get_rvm()
                dictified["affinity"] = planet.get_affinity()

            if planet.type() == "Gas Giant":
                dictified["density"] = planet.get_density()
                dictified["diameter"] = planet.get_diameter()
                dictified["gravity"] = planet.get_gravity()
                dictified["mass"] = planet.get_mass()
                dictified["blackbody_temperature"] = planet.get_blackbody_temp()

            if planet.num_moons() > 0:
                dictified["moons"] = self.encode_moons(planet)
            else:
                dictified["moons"] = []
            dictified["moonlets"] = planet.num_moonlets()
            jsonable.append(dictified)

        return jsonable

    def encode_moons(self, planet):
        if planet.type() == 'Terrestrial':
            moons = planet.get_satellites()
        else:
            moons = planet.get_moons()

        for moon in moons:
            if len(moon.get_name().split('-')) == 3:
                index = moon.get_name().split('-')[2]
                moon.set_name(planet.get_name() + '-' + index)

        jsonable = []
        for moon in moons:
            dictified = dict()
            dictified["name"] = moon.get_name()
            dictified["size"] = moon.get_size()
            dictified["atmospheric_mass"] = moon.get_atmospheric_mass()
            dictified["atmospheric_composition"] = moon.atmcomp
            dictified["atmospheric_pressure"] = moon.get_pressure()
            dictified["pressure_category"] = moon.get_pressure_category()
            dictified["hydrographic_coverage"] = moon.get_hydrographic_cover()
            dictified["avg_surface_temperature"] = moon.get_average_surface_temp()
            dictified["climate"] = moon.get_climate()
            dictified["density"] = moon.get_density()
            dictified["diameter"] = moon.get_diameter()
            dictified["gravity"] = moon.get_gravity()
            dictified["mass"] = moon.get_mass()
            dictified["volcanism"] = moon.get_volcanism()
            dictified["tectonics"] = moon.get_tectonics()
            dictified["resource_value_modifier"] = moon.get_rvm()
            dictified["habitability"] = moon.get_habitability()
            dictified["affinity"] = moon.get_affinity()
            dictified["rotational_period"] = moon.get_rotation()
            jsonable.append(dictified)


        return jsonable
