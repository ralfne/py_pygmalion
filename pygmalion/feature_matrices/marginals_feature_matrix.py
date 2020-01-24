import uuid

from bayesian_network_utilities.api.bayesian_network_wrapper import ProbabilityType
from pygmalion.donors.iterator import GenModelWrapperIterator
import pandas as pd
from pygmalion.genmodel.nicknames import Nicknames


class MarginalsFeatureMatrix(object):
    _INSERTION_COMPOSITION_NICKNAMES = [Nicknames.vj_dinucl.value, Nicknames.vd_dinucl.value, Nicknames.dj_dinucl.value]
    _INSERTION_LENGTHS_NICKNAMES = [Nicknames.vj_ins.value, Nicknames.vd_ins.value, Nicknames.dj_ins.value]


    def __init__(self, items, nicknames, nickname_weights=None, chain=None):
        self._items = items
        self._nicknames = nicknames
        self._nickname_weights = nickname_weights
        self._chain = chain
        self.df = self._create_df()

    def _create_df(self):
        series = []
        itr = GenModelWrapperIterator(self._items, filtering_chain=self._chain)
        names = []
        for gmw in itr:
            bn_wrapper = gmw.get_bayesian_network_wrapper()
            events_serie = self._get_series_for_nicknames(gmw, bn_wrapper)
            series.append(events_serie)
            names.append(gmw.get_name())
        df = pd.concat(series, axis=1)
        df = df.transpose()
        df.index = names
        df = self._standarize(df)
        return df

    def _standarize(self, df):
        factor_col = str(uuid.uuid4())
        df[factor_col] = 1 / df.sum(axis=1)
        cols = []
        series = []
        for n, c in df.iteritems():
            cols.append(n)
            c = c * df[factor_col]
            series.append(c)
        out = pd.concat(series, axis=1)
        out.columns = cols
        out.drop(factor_col, axis=1, inplace=True)
        return out

    def _get_series_for_nicknames(self, genmodel_wrapper, bn_wrapper):
        series = []
        for nickname in self._nicknames:
            if nickname in MarginalsFeatureMatrix._INSERTION_COMPOSITION_NICKNAMES:
                data = genmodel_wrapper.get_insertion_composition(nickname)
                s = pd.Series(data=data, index=self._get_dinucl_keys(nickname))
            elif nickname in MarginalsFeatureMatrix._INSERTION_LENGTHS_NICKNAMES:
                data = genmodel_wrapper.get_insertion_lengths(nickname)
                index_keys = self._get_insertion_lengths_keys(data, nickname)
                s = pd.Series(data=data, index=index_keys)
            else:
                event_name = genmodel_wrapper.get_eventname_for_nickname(nickname)
                s = bn_wrapper.get_probabilities(statename=event_name, probability_type=ProbabilityType.Marginal)
                s = s.sort_index()
            s = self._possibly_calculate_weighted_series(s, nickname)
            series.append(s)
        out = pd.concat(series, axis=0)
        return out

    def _possibly_calculate_weighted_series(self, series, nickname):
        if self._nickname_weights is None:
            return series
        w = self._nickname_weights.get(nickname, None)
        if w is None:
            raise ValueError("Could not find weight for nickname '%s'" % nickname)
        out = series * w
        return out

    def _get_dinucl_keys(self, nickname):
        tmp = ['nucl0', 'nucl1', 'nucl2', 'nucl3']
        out = []
        for s in tmp:
            s = nickname + ':' + s
            out.append(s)
        return out

    def _get_insertion_lengths_keys(self, lengths, nickname):
        out = []
        for i in range(len(lengths)):
            out.append(nickname + ':' + str(i))
        return out

    def add_pseudocounts(self, pseudocount_value=10**-20):
        self.df = self.df + pseudocount_value

