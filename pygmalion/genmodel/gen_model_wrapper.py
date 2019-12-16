import os
from Logger import StdOutLogger
from bayesian_network_utilities.api.bayesian_network_wrapper import BayesianNetworkWrapper
from bayesian_network_utilities.api.distribution_event_merge_definitions import DistributionEventMergeDefinitions
from pygmalion.bayesian_network_importer.bayesian_network_importer import BayesianNetworkImporter
from pygmalion.genmodel.GenModel import GenModel
from pygmalion.genmodel._index_name_guide import _IndexNameGuideList
from pygmalion.genmodel.bayesian_network_merge_utils import BayesianNetworkMergeUtils
from pygmalion.genmodel.nicknames import Nicknames
from pygmalion.markov_chains.steady_state_calculator import SteadyStateCalculator


class GenModelWrapper(object):
    _GENE_NAME_NICKNAMES = ['v_choice', 'j_choice']
    _MARGINALS_DF_COL_NAME = 'Marginal'

    def __init__(self, params_fn, marginals_fn, name='', logger=StdOutLogger(verbose=False)):
        self._logger = logger
        self._params_fn = params_fn
        self._marginal_fn = marginals_fn
        self._name = name
        self._genmodel = GenModel(params_fn, marginals_fn)
        self._logger.log('GenModelWrapper.GenModel class loaded (%s, %s)' % (params_fn, marginals_fn),
                         onlyIfVerbose=True)
        self._init_names_and_nicknames()
        # self._init_guidelist_dict()
        self._insertion_matrices = self._init_insertion_matrices()
        self._network_wrapper = self._init_network_wrapper()
        self._logger.log('GenModelWrapper loaded', onlyIfVerbose=True)
        # self._event_edge_hierarchies = _EventEdgeHierarchies(self._genmodel.edges,
        #                                                      self._nicknames_for_names.keys(),
        #                                                      logger)

    def _init_network_wrapper(self):
        importer = BayesianNetworkImporter(self._logger)
        pg_network = importer.create_network_from_genmodelwrapper(self)
        pg_network.bake()
        wrapper = BayesianNetworkWrapper(pg_network)
        return wrapper

    def _init_insertion_matrices(self):
        calculator = SteadyStateCalculator(self._genmodel.marginals)
        calculator.calculate_for_key('vj_dinucl')
        calculator.calculate_for_key('vd_dinucl')
        calculator.calculate_for_key('dj_dinucl')
        out = calculator.get_matrices()
        return out

    def merge_alleles(self, events=None, prefixes=None):
        d_event = None
        if events is None:
            events =  []
            events.append(self.get_event_from_nickname(Nicknames.v_choice.value))
            events.append(self.get_event_from_nickname(Nicknames.j_choice.value))
            d_event = self.get_event_from_nickname(Nicknames.d_gene.value)
            if d_event is not None: events.append(d_event)
        if prefixes is None:
            prefixes = []
            prefixes.append(Nicknames.v_choice.value + ':')
            prefixes.append(Nicknames.j_choice.value + ':')
            if d_event is not None: prefixes.append(Nicknames.d_gene.value + ':')
        pg_network = BayesianNetworkMergeUtils.create_merged_bayesian_network_for_events(events, prefixes,
                                            self._network_wrapper._network, bake=True, logger=self._logger)
        self._network_wrapper = BayesianNetworkWrapper(pg_network)

    def _init_names_and_nicknames(self):
        self._names_for_nicknames = {}
        self._nicknames_for_names = {}
        for event in self._genmodel.events:
            self._names_for_nicknames[event.nickname] = event.name
            self._nicknames_for_names[event.name] = event.nickname

    def __str__(self):
        return self._name

    # def get_params_and_marginals_fns(self):
    #     return self._params_fn, self._marginals_dfs

    def get_GenModel(self):
        return self._genmodel

    def get_bayesian_network_wrapper(self):
        return self._network_wrapper

    # def _init_guidelist_dict(self):
    #     self._guidelist_dict = {}
    #     for name in self._names_for_nicknames.keys():
    #         gl = self._get_guidelist(name)
    #         self._guidelist_dict[name] = gl
    #
    # def _get_guidelist(self, nickname):
    #     event = self.get_event_from_nickname(nickname)
    #     is_gene_event = event.nickname in GenModelWrapper._GENE_NAME_NICKNAMES
    #     guidelist = _IndexNameGuideList(event, is_gene_event)
    #     return guidelist

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_eventname_for_nickname(self, nickname):
        return self._names_for_nicknames.get(nickname, None)

    def get_event_from_name(self, name):
        for event in self._genmodel.events:
            if event.name == name: return event
        return None

    def get_event_from_nickname(self, nickname):
        for event in self._genmodel.events:
            if event.nickname == nickname: return event
        return None

    def get_bayesian_network_wrapper(self):
        return self._network_wrapper

    def assert_bayesian_network_structure_equality(self, gen_model_wrapper):
        try:
            self._network_wrapper.assert_structure_equality(gen_model_wrapper.get_bayesian_network_wrapper())
        except AssertionError as error:
            id = self._name + 'vs. ' + gen_model_wrapper.get_name() + ': '
            raise AssertionError(id + str(error))
