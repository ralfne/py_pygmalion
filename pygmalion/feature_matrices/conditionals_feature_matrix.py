from bayesian_network_utilities.api.bayesian_network_wrapper import ProbabilityType
import pandas as pd
from pygmalion.genmodel.nicknames import Nicknames

from pygmalion.feature_matrices.marginals_feature_matrix import MarginalsFeatureMatrix


class ConditionalsFeatureMatrix(MarginalsFeatureMatrix):
    def __init__(self, items, nicknames, chain=None):
        super(ConditionalsFeatureMatrix, self).__init__(items=items, nicknames=nicknames, chain=chain)
        illegal_nicknames = [Nicknames.vj_dinucl.value, Nicknames.vd_dinucl.value, Nicknames.dj_dinucl.value,
                             Nicknames.vj_ins.value, Nicknames.vd_ins.value, Nicknames.dj_ins.value]
        intersect = list(set(illegal_nicknames) & set(self._nicknames))
        if len(intersect) != 0:
            raise ValueError('Illegal nickname(s) for ConditionalsFeatureMatrix')

    def _get_series_for_nicknames(self, genmodel_wrapper, bn_wrapper):
        series = []
        for nickname in self._nicknames:
            event_name = genmodel_wrapper.get_eventname_for_nickname(nickname)
            df = bn_wrapper.get_probabilities(statename=event_name, probability_type=ProbabilityType.Conditional)
            s = self._transform_conditional_df_to_series(df.copy())
            s = s.sort_index()
            s = self._possibly_calculate_weighted_series(s, nickname)
            series.append(s)
        out = pd.concat(series, axis=0)
        return out

    def _transform_conditional_df_to_series(self, df):
        df['name'] = df['outcome'] + '; ' + df['conditions']
        df.drop('conditions', axis='columns', inplace=True)
        df.drop('outcome', axis='columns', inplace=True)
        df.set_index('name', inplace=True)
        return df['p']
