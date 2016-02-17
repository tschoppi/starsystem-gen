import random as r


class DiceRoller:

    def roll_dice(self, dice_num, modifier, sides=6) -> int:
        """
        Rolls XdY +- Z.

        :param dice_num: X, the number of dice.
        :param modifier: Z, a static modifier to the result.
        :param sides: Y, the type of dice, defaults to 6-sided.
        :type dice_num: int
        :type modifier: int
        :type sides: int
        :return: A positive int representing the result of the roll.

        In GURPS the dice rolls are always on an interval [0,+infty). As such,
        the lower bound zero will be returned if the modifiers and dice
        combinations turn out to give negative results.
        """

        result = 0
        if sides <= 1:
            raise ValueError("Dice have at least two sides, and not {}.".format(sides))
        if dice_num <= 0:
            raise ValueError("At least 1 die needs to be thrown, not {}.".format(dice_num))
        for i in range(dice_num):
            result += r.randint(1, sides)
        result += modifier
        return max(result, 0)
