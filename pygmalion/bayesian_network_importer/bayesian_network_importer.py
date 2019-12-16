import pomegranate as pg
from Logger import StdOutLogger

from pygmalion.bayesian_network_importer.conditional_matrix import ConditionalMatrix


class BayesianNetworkImporter(object):
    def __init__(self, logger=StdOutLogger(verbose=False)):
        self._logger = logger
        self._gen_model_wrapper = None
        self._gen_model = None

    def create_network_from_genmodelwrapper(self, gen_model_wrapper):
        self._gen_model_wrapper = gen_model_wrapper
        self._gen_model = self._gen_model_wrapper.get_GenModel()
        # self._test_names = ['GeneChoice_V_gene_Undefined_side_prio7_size89',
        #                     'GeneChoice_J_gene_Undefined_side_prio7_size15',
        #                     'GeneChoice_D_gene_Undefined_side_prio6_size3']
        out = pg.BayesianNetwork('')
        self._init_from_gen_model_wrapper(out)
        return out

    def _init_from_gen_model_wrapper(self, bayesian_network):
        matrices = self._create_conditional_matrices()
        self._create_network(matrices, bayesian_network)

    def _create_conditional_matrices(self):
        matrices = {}
        for nickname, marginals_guide in self._gen_model.marginals[1].iteritems():
            event_name = self._gen_model_wrapper.get_eventname_for_nickname(nickname)
            edge = self._gen_model.edges.get(event_name, None)
            if edge is not None:
                # this event is part of the network, ie. not part of cdr3-insertion events
                event = self._gen_model_wrapper.get_event_from_nickname(nickname)
                marginals = self._gen_model.marginals[0].get(nickname)
                cm = ConditionalMatrix(event, self._gen_model_wrapper, marginals, marginals_guide)
                matrices[event_name] = cm
        return matrices

    def _create_network(self, matrices, bayesian_network):
        conditional_probability_tables = self._get_root_conditional_probability_tables(matrices)
        self._add_additional_conditional_probability_tables(conditional_probability_tables, matrices)
        #self._test(matrices)
        states = self._add_network_states(conditional_probability_tables, bayesian_network)
        self._add_network_edges(states, bayesian_network)
        #bayesian_network.bake()

    def _get_root_conditional_probability_tables(self, matrices):
        roots = self._get_root_edges()
        conditional_probability_tables = {}
        for r in roots:
            matrix = matrices.get(r)
            conditional_probability_tables[r] = matrix.get_discrete_distribution()
        return conditional_probability_tables

    def _get_root_edges(self):
        out = []
        edges = self._gen_model.edges
        for name, edge in edges.iteritems():
            if len(edge.parents) == 0:
                out.append(name)
        return out

    def _add_additional_conditional_probability_tables(self, conditional_probability_tables, matrices):
        ok = False
        while not ok:
            ok = self._try_get_conditional_probability_tables(conditional_probability_tables, matrices)

    def _try_get_conditional_probability_tables(self, conditional_probability_tables, matrices):
        all_ok = True
        for nickname, marginals_guide in self._gen_model.marginals[1].iteritems():
            name = self._gen_model_wrapper.get_eventname_for_nickname(nickname)
            edge = self._gen_model.edges.get(name, None)
            cpt = conditional_probability_tables.get(name, None)
            if (edge is not None) and (cpt is None):
                matrix = matrices.get(name, None)
                ok = self._possibly_add_conditional_probability_tables_for_event(marginals_guide,
                                                                matrix, conditional_probability_tables)
                if not ok: all_ok = False
        return all_ok

    def _possibly_add_conditional_probability_tables_for_event(self, marginals_guide, matrix,
                                                                conditional_probability_tables):
        for i in range(len(marginals_guide)):
            nickname = marginals_guide[i]
            name = self._gen_model_wrapper.get_eventname_for_nickname(nickname)
            cpt = conditional_probability_tables.get(name, None)
            if cpt is None:
                cpt = matrix.get_conditional_probability_table(conditional_probability_tables)
                if cpt is None: return False
                conditional_probability_tables[name] = cpt
        return True

    def _add_network_states(self, conditional_probability_tables, bayesian_network):
        states = {}
        for key, cpt in conditional_probability_tables.iteritems():
            state = pg.State(cpt, name=key)
            bayesian_network.add_state(state)
            states[key] = state
        return states

    def _add_network_edges(self, states, bayesian_network):
        edges = self._gen_model_wrapper.get_GenModel().edges
        for name, edge in edges.iteritems():
            for childname in edge.children:
                st1 = states.get(name)
                st2 = states.get(childname)
                bayesian_network.add_edge(st1, st2)
