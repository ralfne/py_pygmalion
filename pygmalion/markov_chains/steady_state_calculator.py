from discreteMarkovChain import markovChain
import numpy as np


class SteadyStateCalculator(object):
    def __init__(self, genmode_marginals):
        self._marginals = genmode_marginals
        self._matrices = {}

    def calculate_for_key(self, key):
        matrix = self._marginals[0].get(key, None)
        if matrix is not None:
            matrix = SteadyStateCalculator._format_as_4x4_matrix(matrix)
            steady_state = SteadyStateCalculator._calculate(matrix)
            self._matrices[key] = steady_state

    def get_matrices(self):
        return self._matrices

    @staticmethod
    def _format_as_4x4_matrix(vector):
        x = np.asarray(vector)
        array = x.reshape(4, 4)
        return array

    @staticmethod
    def _calculate(matrix):
        mc = markovChain(matrix)
        mc.computePi('linear')
        out = mc.pi
        return out
