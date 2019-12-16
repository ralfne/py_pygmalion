from Logger import StdOutLogger
from immune_receptor_utils import enums as ir

from pygmalion.genmodel.gen_model_wrapper import GenModelWrapper


class Donor(object):
    def __init__(self, cell_filenames, name=None, logger=StdOutLogger(False)):
        self._logger = logger
        self._name = name
        self._chain_models = {}
        for c in ir.Chain:
            params_fn = cell_filenames.get_params_fn(c)
            marginals_fn = cell_filenames.get_marginals_fn(c)
            if (params_fn is None) and (params_fn is None):
                pass
            elif (params_fn is not None) and (params_fn is not None):
                self._chain_models[c] = GenModelWrapper(params_fn, marginals_fn, self._get_model_name(c), self._logger)
                if self._name is None:
                    self._name = self._chain_models[c].get_name()
                self._logger.log('%s GenModelWrapper loaded' % str(c), includeTimestamp=False, onlyIfVerbose=True)
            else:
                raise ValueError('donors filenames corrupt')

    def __str__(self):
        return self._name

    def _get_model_name(self, chain):
        return self._name + '_' + str(chain)

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_genmodel_wrapper(self, tcr_chain):
        return self._chain_models.get(tcr_chain, None)

    def get_chains(self):
        return self._chain_models.keys()
