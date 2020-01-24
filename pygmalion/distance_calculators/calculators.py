from abc import ABCMeta, abstractmethod

import scipy
from scipy.spatial import distance
import pandas as pd
import numpy as np
from scipy.spatial.distance import squareform
from scipy.stats import entropy


class DistanceCalculator(object):
    __metaclass__ = ABCMeta

    def __init__(self):pass

    @abstractmethod
    def run(self, data):pass

    def _get_pairs(self, data):
        index = data.index
        l_index = len(index)
        out = np.zeros((l_index, l_index))
        for i in range(l_index - 1):
            for j in range(i + 1, l_index):
                s0 = data.loc[index[i]]
                s1 = data.loc[index[j]]
                y = self._run_for_series(s0, s1)
                out[i, j] = y
        i_lower = np.tril_indices(l_index, -1)
        out[i_lower] = out.T[i_lower]
        out = pd.DataFrame(out, index=index, columns=index)
        return out


class SpatialCDistCalculator(DistanceCalculator):
    def __init__(self, metric, **kwargs):
        super(SpatialCDistCalculator, self).__init__()
        self._metric = metric
        self._kwargs = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                self._kwargs[key] = value

    def run(self, data):
        out = distance.pdist(data, self._metric,  **self._kwargs)
        pairwise = pd.DataFrame(squareform(out), columns=data.index, index=data.index)
        return pairwise


class JensenShannonCalculator(DistanceCalculator):
    def __init__(self, base=2):
        super(JensenShannonCalculator, self).__init__()
        self._base = base

    def run(self, data):
        # out=0
        # if isinstance(data, WeightedFeatureMatrices):
        #     for i in len(data):
        #         matrix = data.get_matrix(i)
        #         weight = data.get_weight(i)
        #         score = self._run_for_feature_matrix(matrix)
        #         out += score * weight
        # elif isinstance(data, pd.DataFrame):
        #     score = self._run_for_feature_matrix(data)
        #     out += score
        # else:
        #     raise NotImplementedError()
        if isinstance(data, pd.DataFrame):
            out = self._get_pairs(data)
        else:
            raise NotImplementedError()
        return out

    # def _run_for_feature_matrix(self, matrix):
    #     out = self._get_pairs(matrix)
    #     return out

    def _run_for_series(self, series1, series2):
        out = self._calculate_jensen_shannon(series1, series2)
        return out

    def _calculate_jensen_shannon(self, p, q):
        # could not install scipy version 1.5 which contains the jensen-shannon func;
        # using solution from https://gist.github.com/zhiyzuo/f80e2b1cfb493a5711330d271a228a3d
        p = np.asarray(p)
        q = np.asarray(q)
        # normalize
        p /= p.sum()
        q /= q.sum()
        m = (p + q) / 2
        return (entropy(p, m, base=self._base) + entropy(q, m, self._base)) / 2


class EuclideanDistanceCalculator(DistanceCalculator):
    def __init__(self):
        super(EuclideanDistanceCalculator, self).__init__()

    def run(self, data):
        if isinstance(data, pd.DataFrame):
            out = self._get_pairs(data)
        else:
            raise NotImplementedError()
        return out

    def _run_for_series(self, series1, series2):
        out = distance.euclidean(series1, series2)
        return out


class SymmetricKullbackLeiblerCalculator(DistanceCalculator):
    def __init__(self, base=2):
        super(SymmetricKullbackLeiblerCalculator, self).__init__()
        self._base = base

    def run(self, data):
        if isinstance(data, pd.DataFrame):
            out = self._get_pairs(data)
        else:
            raise NotImplementedError()
        return out

    def _run_for_series(self, series1, series2):
        out = self._calculate_symmetric_kld(series1, series2)
        return out

    def _calculate_symmetric_kld(self, p, q):
        kullback_leibler = scipy.stats.entropy(p, q, base=self._base)
        kullback_leibler_2 = scipy.stats.entropy(p, q, base=self._base)
        kullback_leibler += kullback_leibler_2
        return kullback_leibler
