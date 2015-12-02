import random


class MarkovStateFactory:
    """
    Keeps a copy of all MarkovStates, so that only one is ever created for any given value.
    :type __states: dict[str, MarkovState]
    """
    __states = dict()

    def get_markov_state(self, value):
        key = ""
        if len(value) < 1:
            value = ["@"]
        for s in value:
            key += s
        if key in self.__states:
            return self.__states[key]
        else:
            state = MarkovState(value)
            self.__states[key] = state
            return state

    def reset_states(self):
        self.__states = dict()


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

    def next_state(self):
        """
        Returns the value of the next state.
        """
        # FIXME: This should return the state directly. However, that means that this needs to store the states too...
        if len(self.transitions) > 0:
            return self.transitions[random.randint(0, len(self.transitions) - 1)]
        else:
            arr = []
            for i in range(1, self.depth):
                arr.append("@")
            return arr

    def add_transition(self, value):
        self.transitions.append(value)


class MarkovStateMachine:
    """
    :type currentState: MarkovState
    :type startState: MarkovState
    :type depth: int
    """

    factory = MarkovStateFactory()

    def __init__(self, depth=1):
        if depth < 1:
            depth = 1
        self.depth = depth
        start_array = []
        for _ in range(0, depth):
            start_array.append("@")
        # Start with an invalid / 'starting' character.
        self.startState = self.factory.get_markov_state(start_array)
        self.currentState = self.factory.get_markov_state(start_array)

    def next(self) -> None:
        self.currentState = self.factory.get_markov_state(self.currentState.next_state())

    def get_letter(self) -> str:
        return self.currentState.value[-1]  # Retrieves the last letter of the window, which is the newest.

    def add_transitions(self, word) -> None:
        """
        Add the letter-to-letter transitions based on the given word.
        :param word: A string to be parsed
        :type word: str
        """
        for letter in word.lower():
            if self.depth == 1:  # There is no need to keep a moving window, simplifying this code.
                self.currentState.add_transition([letter])
                self.currentState = self.factory.get_markov_state(self.currentState.transitions[-1])
            else:
                # This produces a moving window of size depth, allowing for some pattern finding.
                new_array = list(self.currentState.value)
                if len(new_array) == self.depth:
                    new_array.pop(0)
                new_array.append(letter)
                self.currentState.add_transition(new_array)
                self.currentState = self.factory.get_markov_state(self.currentState.transitions[-1])
        self.reset_state()

    def analyze_text(self, text, initialize=True) -> None:
        """
        Generate the transition rules for a markov chain, based on the given text.
        :param text: A list of words to be parsed.
        :param initialize: If False, the transitions are merely updated, enlarging the corpus
        :type text: list[str]
        :type initialize: bool
        :return: None
        """
        if initialize:
            self.factory.reset_states()  # It's a factory reset! :D Deletes all states, and thus all loaded transitions.
            arr = []
            for _ in range(0, self.depth):
                arr.append("@")
            self.currentState = self.factory.get_markov_state(arr)
        for word in text:
            self.add_transitions(word)

    def reset_state(self) -> None:
        """
        Go back to the starting state. This doesn't reset the transitions! It is therefore used to process or generate a new word.
        :return: None
        """
        self.currentState = self.startState

    def get_name(self, length=0) -> str:
        """
        Uses get_letter() to generate names of length 3-8, or any specified, positive length.
        :param length: Integer length of the name to be generated.
        :type length: int
        :return: A capitalized name.
        """
        if length < 0:
            length = 0
        if length == 0:
            length = random.randint(3, 8)
        result = ""
        while len(result) < length:
            self.next()
            if self.get_letter().isalpha():  # No bias towards making syllables; regular letters are just added.
                result += self.get_letter()
            elif not self.get_letter() == "@" and len(result) > 1 and length - len(result) > 2:
                # Punctuation is never the first letter nor one of the last two letters. Looks better
                result += self.get_letter()
            else:  # Restart the chain, since the last letter was a word-end and the output is still too short.
                self.reset_state()
        # In some of the corpuses, a name can contain spaces and all parts must be capitalized.
        # See for example La Paz vs La paz or La Coru�a vs La coru�a.
        temp = [string.capitalize() for string in result.split(" ")]
        result = ""
        for string in temp:
            result += string + " "
        return result.strip(" ")  # Trailing spaces must be stripped, too.
