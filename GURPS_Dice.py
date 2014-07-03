import random as r

class DiceRoller:
	def roll(self, dicenum, modifier):
		result = 0
		for i in range(dicenum):
			result += r.randint(1,6)
		result += modifier
		return result
