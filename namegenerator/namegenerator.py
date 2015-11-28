import csv
import random
import os
import string
from .markovchain import MarkovStateMachine


class NameGenerator:

    names = []

    loaded_file = ()
    reload_counter = 0

    corpus = ""

    markov_chain = MarkovStateMachine()

    use_chain = False

    suffixes = ['', '-Beta', '-Gamma']

    def set_corpus(self, corpus):
        self.corpus = corpus

    def read_file(self, path):
        """
            Loads prepared names or seeds for the markov chain from a file.
            :param path: The file name to read
            :type path: str
        """
        self.names = []
        self.loaded_file = path
        path = os.path.dirname(os.path.realpath(__file__)) + '/corpuses/' + path
        if path:
            with open(path, newline='', encoding='utf-8') as csv_file:
                corpus_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
                for row in corpus_reader:
                    self.names.append(*row)
        self.markov_chain.analyze_text(self.names)

    def reload_file(self):
        """
            Reloads the corpus, used when the pre-generated names run out. Increases the reload counter, so that an appropriate suffix is used for new names.
        """
        self.read_file(self.loaded_file)
        self.reload_counter += 1

    def list_available_corpuses(self):
        """
            Returns a generator for the available corpuses. These corpuses contain names that belong to a given theme and need no further
            mangling to be useable. However, they can also be used as seeds for a markov chain.
            :return: A generator object for a list of the available corpuses.
        """
        corpuses_dir = os.path.dirname(os.path.realpath(__file__)) + '/corpuses'
        for file in os.listdir(corpuses_dir):
            if file.endswith('.csv'):
                yield (file)

    def get_random_name(self):
        """
            Get a name from the name generator.
            :return: Return a name, either from the corpus or generate by the markov chain.
        """
        if self.use_chain:
            return self.markov_chain.get_name()
        else:
            result = self.names.pop(random.randint(0, len(self.names)-1))[0] + self.suffixes[self.reload_counter]
            if len(self.names) == 0:
                self.reload_file()
            return result

    def generate_pseudoscientific_name(self, star, planet):
        # FIXME: This is not yet in a useable state.
        star_part = star.get_sequence()[0] + '-' + star.get_letter()
        if int(planet.get_name()[-2] == 0):
            planet_part = planet.type()[:2] + planet.get_name()[-3:-2]
        else:
            planet_part = planet.type()[:2] + planet.get_name()[-2]
        if planet.type() != 'Gas Giant':
            planet_part = planet_part + '-' + planet.get_type()[:3]
        return star_part + '-' + planet_part

