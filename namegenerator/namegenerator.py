import csv
import random
import os


class NameGenerator:

    names = []

    """
        Loads prepared names or seeds for the markov chain from a file.
        Keyword arguments:
        path -- the file name, must be provided
        seed_or_corpus -- 'seeds' or 'corpuses', depending on what is to be read. Defaults to 'corpuses'.
    """
    def read_file(self, path, seed_or_corpus='corpuses'):
        self.names = []
        path = os.path.dirname(os.path.realpath(__file__)) + '/' + seed_or_corpus + '/' + path
        if path:
            with open(path, newline='', encoding='utf-8') as csv_file:
                corpus_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
                for row in corpus_reader:
                    self.names.append(row)

    """
        Returns a generator for the available corpuses of pre-prepared names.
        These corpuses contain names that belong to a given theme and need no further
        mangling to be useable.
    """
    def list_available_corpuses(self):
        corpuses_dir = os.path.dirname(os.path.realpath(__file__)) + '/corpuses'
        for file in os.listdir(corpuses_dir):
            if file.endswith('.csv'):
                yield (file)

    """
        Returns a generator for the available seed files.
        These seeds will be syllables or even characters, possibly weighted, so
        that they can be fed to a markov chain and names generated from them.
    """
    def list_available_seeds(self):
        seeds_dir = os.path.dirname(os.path.realpath(__file__)) + '/seeds'
        for file in os.listdir(seeds_dir):
            if file.endswith('.csv'):
                yield (file)

    """
        Returns a random name from the available names.
    """
    def get_random_name(self):
        if len(self.names) > 0:
            return self.names.pop(random.randint(0, len(self.names)-1))[0]
        else:
            return 'used all names up!'

    def generate_name(self):
        # TODO: Generate a name from a seed using a markov chain
        return "RANDOMNESS!!"

    """
        Returns a name based on the star and planet details.
        Keyword arguments:
            star -- the star that the named body orbits
            planet -- the planet to be named
    """
    def generate_pseudoscientific_name(self, star, planet):
        star_part = star.get_sequence()[0] + '-' + star.get_letter()
        planet_part = planet.type()[:2]
        if int(planet.get_name()[-2] == 0):
            planet_part = planet.type()[:2] + planet.get_name()[-3:-2]
        else:
            planet_part = planet.type()[:2] + planet.get_name()[-2]
        if planet.type() != 'Gas Giant':
            planet_part = planet_part + '-' + planet.get_type()[:3]
        return star_part + '-' + planet_part
