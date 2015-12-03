import unittest
from namegenerator import namegenerator


class TestNameGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = namegenerator.NameGenerator()
        self.generator.read_file("../../tests/test_corpus.csv")

    def test_reload(self):
        self.assertEqual("mark", self.generator.get_random_name())
