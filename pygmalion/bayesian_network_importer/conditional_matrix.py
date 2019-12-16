from copy import deepcopy
import pomegranate as pg
import numpy as np
from immune_receptor_utils import utilities


class _ConditionalMatrixParents(object):
    def __init__(self, gen_model_wrapper, marginals_guide):
        self._gen_model_wrapper = gen_model_wrapper
        self._items = []
        for i in range(len(marginals_guide)-2, -1, -1):
            m = marginals_guide[i]
            self._items.append(m)

    def __iter__(self):
        return self._items.__iter__()

    def __len__(self):
        return self._items.__len__()

    def get_parent(self, index, default, reverse):
        if (index >= len(self._items)) or (index < 0):
            out = default
        else:
            if reverse:
                index2 = (len(self._items) - 1) - index
                out = self._items[index2]
            else:
                out = self._items[index]
        return out

    def get_parents_table(self, conditional_probability_table):
        out = []
        for i in range(len(self._items)-1, -1, -1):
            p = self._items[i]
            name = self._gen_model_wrapper.get_eventname_for_nickname(p)
            cpt = conditional_probability_table.get(name, None)
            if cpt is None: return None
            out.append(cpt)
        return out


class _ConditionalMatrixRow(object):
    def __init__(self, event, marginals, parents, gen_model_wrapper, use_realization_names):
        self._event = event
        self._marginals = marginals
        self._parents = parents
        self._use_realization_names = use_realization_names
        self._gen_model_wrapper = gen_model_wrapper
        self._items = []
        self._add_rows()

    def _add_rows(self):
        sizes = self._get_parent_sizes(self._parents)
        no_of_rows = self._get_product(sizes)
        no_of_rows *= len(self._event.realizations)
        indices = [0]
        for p in self._parents:
            indices.append(0)
        parents_index = [len(self._parents)-1]
        self._update_indices(self._marginals, indices, parents_index)

    def _get_marginal_from_indices(self, indices):
        for row in self._items:
            if row[0:3] == indices:
                return row[len(row)-1]
        return None

    def _update_indices(self, current_marginal, indices, parents_index):
        for i in range(len(current_marginal)):
            current_marginal_value = current_marginal[i]
            if isinstance(current_marginal[i], np.ndarray):
                self._update_indices(current_marginal_value, indices, parents_index)
                indices[parents_index[0]] += 1
            else:
                self._enter_marginal_values(indices, current_marginal)
                indices[len(indices)-1] = 0
                return
        indices[parents_index[0]] = -1
        indices[parents_index[0]-1] = indices[parents_index[0]-1] + 1

    def _enter_marginal_values(self, indices, current_marginal):
        for i in range(len(current_marginal)):
            current_marginal_value = current_marginal[i]
            tmp = deepcopy(indices)
            tmp.append(current_marginal_value)
            for j in range(len(tmp)-1):
                tmp[j] = self._get_marginal_id(tmp[j], j)
            self._items.append(tmp)
            last_index_value = indices[len(indices)-1]
            indices[len(indices)-1] = last_index_value+1

    def _get_marginal_id(self, index, parent_index):
        if self._use_realization_names:
            parent_nickname = self._parents.get_parent(parent_index, default=None, reverse=True)
            if parent_nickname is None:
                current_nickname = self._event.nickname
            else:
                current_nickname = parent_nickname
            event = self._gen_model_wrapper.get_event_from_nickname(current_nickname)
            realization = event.realizations[index]
            if realization.name.strip() == '':
                out = str(realization.value)
            else:
                out = realization.name.strip()
                if current_nickname in ConditionalMatrix.GENE_NAME_NICKNAMES:
                    out = utilities.extract_tcr_gene_string(out)
            out = current_nickname + ConditionalMatrix.EVENT_NICKNAME_REALIZATION_SEP + out
        else:
            out = str(index)

        return out

    def _get_parent_sizes(self, parents):
        parents_sizes = {}
        for p in parents:
            event = self._gen_model_wrapper.get_event_from_nickname(p)
            s = len(event.realizations)
            parents_sizes[p] = s
        return parents_sizes

    def _get_product(self, numbers_dict):
        out = 1
        for key, value in numbers_dict.iteritems():
            out *= value
        return out

    def get_table(self):
        return self._items

    def get_dict(self):
        out = {}
        for r in self._items:
            out[str(r[0])] = r[1]
        return out


class ConditionalMatrix(object):
    EVENT_NICKNAME_REALIZATION_SEP = ':'
    GENE_NAME_NICKNAMES = ['v_choice', 'j_choice', 'd_gene']

    def __init__(self, event, gen_model_wrapper, marginals, marginals_guide):
        self._event = event
        self._gen_model_wrapper = gen_model_wrapper
        self._parents = _ConditionalMatrixParents(self._gen_model_wrapper, marginals_guide)
        self._rows = _ConditionalMatrixRow(self._event, marginals, self._parents,
                                           self._gen_model_wrapper, use_realization_names=True)

    def get_root_state(self):
        if len(self._parents) != 0: raise ValueError('Not a root state')
        p = pg.DiscreteDistribution(self._rows.get_dict())
        out = pg.State(p, name=self._name)
        return out

    def get_discrete_distribution(self):
        out = pg.DiscreteDistribution(self._rows.get_dict())
        return out

    def get_conditional_probability_table(self, conditional_probability_table):
        tbl = self._rows.get_table()
        cpts = self._parents.get_parents_table(conditional_probability_table)
        if cpts is None: return None
        out = pg.ConditionalProbabilityTable(tbl, cpts)
        return out
