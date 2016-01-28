import random


class MarkovState:
    """
    :type transitions: list[list[str]]
    :type value: list[str]
    :type depth: int
    """

    value = [""]
    depth = 1

    def __init__(self, value):
        """
        Represents a state in the markov chain.
        :param value: The letter that this state represents.
        :type value: list[str]
        """
        self.value = value
        self.depth = len(value)
        self.transitions = []

    def __str__(self):
        retval = "MarkovState:"
        for s in self.value:
            retval += " "
            retval += s
        return retval

    def __eq__(self, other):
        return self.value == other.value

    def next_state(self) -> [str]:
        """
        Returns the value of the next state.
        """
        if len(self.transitions) > 0:
            return self.transitions[random.randint(0, len(self.transitions) - 1)]
        else:
            arr = []
            for i in range(1, self.depth):
                arr.append("@")
            return arr

    def add_transition(self, value) -> None:
        """
        Stores a new transition from this state to the state given by value.
        :param value: The value of the target state.
        """
        self.transitions.append(value)
