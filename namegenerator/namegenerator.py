import csv
import random
import os

from .markovchain import MarkovStateMachine


class NameGenerator:
    """
    Can either select names from a prepared corpus or use that as a basis for a markov chain of random names.
    :type names: list[string]
    :type loaded_file:
    :type reload_counter: int
    :type markov_chain: MarkovStateMachine
    :type corpus: str
    :type use_chain: Boolean
    :type suffixes: list[str]
    """

    names = []

    loaded_file = ()
    reload_counter = 0

    corpus = ""

    markov_chain = MarkovStateMachine()

    use_chain = False

    suffixes = ['', '-Beta', '-Gamma']

    def __init__(self, depth=1):
        self.markov_chain = MarkovStateMachine(depth)

    def set_corpus(self, corpus) -> None:
        self.corpus = corpus

    def read_file(self, path) -> None:
        """
            Loads prepared names and seeds for the markov chain from a file.
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

    def reload_file(self) -> None:
        """
            Reloads the corpus, used when the pre-generated names run out. Increases the reload counter, so that an appropriate suffix is used for new names.
        """
        self.read_file(self.loaded_file)
        self.reload_counter += 1

    @staticmethod
    def list_available_corpuses() -> [str]:
        """
            Returns a generator for the available corpuses. These corpuses contain names that belong to a given theme and need no further
            mangling to be usable. However, they can also be used as seeds for a markov chain.
            :return: A generator object for a list of the available corpuses.
        """
        corpuses_dir = os.path.dirname(os.path.realpath(__file__)) + '/corpuses'
        for file in os.listdir(corpuses_dir):
            if file.endswith('.csv'):
                yield (file)

    def get_random_name(self) -> str:
        """
            Get a name from the name generator.
            :return: Return a name, either from the corpus or generate by the markov chain.
        """
        if self.use_chain:
            return self.markov_chain.get_name()
        else:
            result = self.names.pop(random.randint(0, len(self.names)-1)) + self.suffixes[self.reload_counter]
            if len(self.names) == 0:
                self.reload_file()
            return result


