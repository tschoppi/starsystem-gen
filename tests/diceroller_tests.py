import unittest
from gurpsspace import dice

class TestDiceRoller(unittest.TestCase):

    def setUp(self):
        self.roller = dice.DiceRoller()

    def test_roll_non_negative_returns(self):
        self.assertEqual(self.roller.roll(dice_num=1, modifier=-7, sides=6), 0)
