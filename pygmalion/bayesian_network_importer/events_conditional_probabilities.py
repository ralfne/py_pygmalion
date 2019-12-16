class EventsConditionalProbabilities(object):
    def __init__(self, nickname, state, gen_model_wrapper):
        self._state = state
        gen_model = gen_model_wrapper.get_GenModel()
        self._parents = gen_model.marginals[1].get(nickname)

    def get_as_list(self):
        return self._state.distribution.parameters[0]

    def get_parents(self):
        return self._parents