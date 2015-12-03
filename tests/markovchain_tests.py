import unittest
import namegenerator.markovchain


class TestMarkovChain(unittest.TestCase):

    def setUp(self):
        self.markov_chain = namegenerator.markovchain.MarkovStateMachine()
        self.markov_chain.analyze_text(["mark", "mark", "mark"])

    def test_get_name_with_single_name_input(self):
        self.assertEqual("Mark", self.markov_chain.get_name(4))
