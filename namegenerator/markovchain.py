import random


class MarkovState:
    """
    :type transitions: list[MarkovState]
    :type value: str
    """

    transitions = []
    value = ""

    def __init__(self, value):
        """
        Represents a state in the markov chain.
        :param value: The letter that this state represents.
        """
        self.value = value

    def __str__(self):
        return self.value

    def next_state(self):
        if len(self.transitions) > 0:
            return self.transitions[random.randint(0, len(self.transitions) - 1)]
        else:
            return MarkovState("")

    def add_transition(self, state):
        self.transitions.append(state)


class MarkovStateMachine:
    """
    :type startState: MarkovState
    :type currentState: MarkovState
    """

    startState = MarkovState("")
    currentState = startState

    def next(self) -> None:
        self.currentState = self.currentState.next_state()

    def get_letter(self) -> str:
        return self.currentState.value

    def add_transitions(self, word) -> None:
        """
        Add the letter-to-letter transitions based on the given word.
        :param word: A string to be parsed
        :type word: str
        """
        for letter in word.lower():
            self.currentState.add_transition(MarkovState(letter))
            self.currentState = MarkovState(letter)
        self.reset_state()

    def analyze_text(self, text, initialize=True) -> None:
        """
        Generate the transition rules for a markov chain, based on the given text.
        :param text: A list of words to be parsed.
        :param initialize: If False, the transitions are merely updated, adding another corpus
        :type text: list[str]
        :type initialize: bool
        :return: None
        """
        if initialize:
            self.currentState = MarkovState("")
        for word in text:
            print(word)
            self.add_transitions(word)

    def reset_state(self) -> None:
        """
        Go back to the starting state. This doesn't reset the transitions! It is therefore used to process or generate a new word.
        :return: None
        :rtype: None
        """
        self.currentState = self.startState

    def get_name(self, length=0) -> str:
        if length == 0:
            length = random.randint(3, 8)
        result = ""
        while len(result) < length:
            self.next()
            result += self.get_letter()
        return result.capitalize()

