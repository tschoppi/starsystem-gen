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
        Returns a random name from the available names.
    """
    def get_random_name(self):
        return self.names.pop(random.randint(0, len(self.names)-1))

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

    def generate_name(self):
        # TODO: Generate a name from a seed using a markov chain
        return "RANDOMNESS!!"

    def generate_pseudoscientific_name(self, star, planet, is_moon=False, moon=None):
        return "SCIENCE!"
        # TODO: generate name based on star and planet classifications


# Debugging code to see whether stuff works. TODO: remove this before release
gen = NameGenerator()
for i in gen.list_available_corpuses():
    gen.read_file(i)
    print(gen.get_random_name())
