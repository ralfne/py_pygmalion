class MarginalsIndicesMap(object):
    def __init__(self, gen_model_wrapper):
        self._map = {}
        for event in gen_model_wrapper.get_GenModel().events:
            event_map = {}
            self._map[event.name] = event_map
            for i, r in enumerate(event.realizations):
                event_map[r.index] = i

    def get_index(self, event, index):
        event_map = self._map.get(event.name)
        out = event_map.get(index)
        return out
