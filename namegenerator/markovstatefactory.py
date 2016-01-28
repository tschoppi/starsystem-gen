from namegenerator.markovstate import MarkovState


class MarkovStateFactory:
    """
    Keeps a copy of all MarkovStates, so that only one is ever created for any given value.
    :type __states: dict[str, namegenerator.markovstate.MarkovState]
    """
    __states = dict()

    def get_markov_state(self, value):
        """
        Provides the MarkovState corresponding to the given value. Only creates a new MarkovState once per value.
        :param value: The character(s) that the MarkovState represents.
        :type value: list[str]
        :return: An instance of MarkovState.
        """
        key = ""
        if len(value) < 1:
            value = ["@"]
        for s in value:
            key += s
        # value is a list, which is not itself hashable for use as a dictionary key.
        # Its values are joined as a key instead.
        if key in self.__states:
            return self.__states[key]
        else:
            state = MarkovState(value)
            self.__states[key] = state
            return state

    def reset_states(self) -> None:
        """
        Forget all generated MarkovStates, therefore also forgetting all previous transitions.
        """
        self.__states = dict()
