import random as r


class DiceRoller:
    def roll(self, dice_num, modifier, sides=6) -> int:
        """
        Rolls XdY +- Z.
        :param dicenum: X, the number of dice.
        :param modifier: Z, a static modifier to the result.
        :param sides: Y, the type of dice, defaults to 6-sided.
        :type dice_num: int
        :type modifier: int
        :type sides: int
        :return: An int representing the result of the roll.
        """
        result = 0
        for i in range(dice_num):
            result += r.randint(1, sides)
        result += modifier
        return result
