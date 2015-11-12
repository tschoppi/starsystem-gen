import csv
import random
import os


class NameGenerator:

    names = []

    def read_file(self, path):
        path = os.path.dirname(os.path.realpath(__file__)) + '/corpuses/' + path
        if path:
            with open(path, newline='', encoding='utf-8') as csv_file:
                corpus_reader = csv.reader(csv_file, delimiter=',', skipinitialspace=True)
                for row in corpus_reader:
                    self.names.append(row)

    def get_random_name(self):
        return self.names.pop(random.randint(0, len(self.names)-1))

    def list_available_corpuses(self):
        corpuses_dir = os.path.dirname(os.path.realpath(__file__)) + '/corpuses'
        for file in os.listdir(corpuses_dir):
            if file.endswith('.csv'):
                yield (file)


# Debugging code to see whether stuff works. TODO: remove this before release
gen = NameGenerator()
for i in gen.list_available_corpuses():
    gen.read_file(i)
    print(gen.get_random_name())
