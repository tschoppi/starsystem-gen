import unittest
from namegenerator import namegenerator


class TestNameGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = namegenerator.NameGenerator(1, 1)  # Fixed depth and seed

    def test_get_random_name_select_one_name(self):
        self.generator.read_file("../../tests/test_corpus_one_name.csv")
        self.assertEqual("mark", self.generator.get_random_name())

    def test_file_reloaded_when_corpus_empty(self):
        self.generator.read_file("../../tests/test_corpus_one_name.csv")
        i = 0
        while i < 10:
            self.generator.get_random_name()
            i += 1
        self.assertTrue(self.generator.reload_counter > 0)
        self.assertEqual(self.generator.reload_counter, 2)

    def test_suffix_selected_after_reload(self):
        self.generator.read_file("../../tests/test_corpus_one_name.csv")
        self.generator.reload_file()
        self.assertTrue(self.generator.get_random_name().endswith("-Beta"))

    def test_markov_generation(self):
        self.generator.read_file("roman.csv")
        self.generator.use_chain = True
        self.assertEqual("Vesaptan", self.generator.get_random_name(8))
