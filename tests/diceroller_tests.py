import unittest
from gurpsspace import dice


class TestDiceRoller(unittest.TestCase):

    def setUp(self):
        self.roller = dice.DiceRoller()

    def test_roll_non_negative_returns(self):
        self.assertEqual(self.roller.roll_dice(dice_num=1, modifier=-7, sides=6), 0)

    def test_roll_negative_sided_die(self):
        self.assertRaises(ValueError, self.roller.roll_dice, dice_num=1, modifier=0, sides=-1)

    def test_roll_zero_sided_die(self):
        self.assertRaises(ValueError, self.roller.roll_dice, dice_num=1, modifier=0, sides=0)

    def test_roll_one_sided_die(self):
        self.assertRaises(ValueError, self.roller.roll_dice, dice_num=1, modifier=0, sides=1)

    def test_roll_zero_dice(self):
        self.assertRaises(ValueError, self.roller.roll_dice, dice_num=0, modifier=0)

    def test_roll_negative_dice(self):
        self.assertRaises(ValueError, self.roller.roll_dice, dice_num=-1, modifier=0)
