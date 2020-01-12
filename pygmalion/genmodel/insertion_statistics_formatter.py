from pygmalion.genmodel.nicknames import Nicknames


class InsertionStatisticsFormatter(object):
    _LENGTHS = {Nicknames.vj_ins.value: 41, Nicknames.vd_ins.value: 31, Nicknames.dj_ins.value: 31}

    def __init__(self, genmodelwrapper):
        self._genmodelwrapper = genmodelwrapper
        self._stats = {}
        nickname = Nicknames.vj_ins.value
        stats = self._format(nickname)
        if stats is not None:
            self._stats[nickname] = stats
        nickname = Nicknames.vd_ins.value
        stats = self._format(nickname)
        if stats is not None:
            self._stats[nickname] = stats
        nickname = Nicknames.dj_ins.value
        stats = self._format(nickname)
        if stats is not None:
            self._stats[nickname] = stats

    def get_lengths_statistics(self):
        return self._stats

    def _format(self, nickname):
        length = InsertionStatisticsFormatter._LENGTHS.get(nickname)
        guide = self._create_guide_dict(nickname)
        if guide is None:
            out = None
        else:
            out = []
            genmodel = self._genmodelwrapper.get_GenModel()
            margs = genmodel.marginals[0].get(nickname)
            for i in range(length):
                index = guide.get(i, None)
                if index is None:
                    m = 0.0
                else:
                    m = margs[index]
                out.append(m)
        return out

    def _create_guide_dict(self, nickname):
        out = {}
        event = self._genmodelwrapper.get_event_from_nickname(nickname)
        if event is None:
            return None
        else:
            for i, r in enumerate(event.realizations):
                out[r.index] = i
        return out
