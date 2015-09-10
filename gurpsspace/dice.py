import random as r


class DiceRoller:
    def roll(self, dice_num, modifier, sides=6):
        result = 0
        for i in range(dice_num):
            result += r.randint(1, sides)
        result += modifier
        return result
