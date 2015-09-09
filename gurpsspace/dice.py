import random as r


class DiceRoller:
    def roll(self, dice_num, modifier):
        result = 0
        for i in range(dice_num):
            result += r.randint(1, 6)
        result += modifier
        return result
