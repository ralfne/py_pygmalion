from abc import ABCMeta, abstractmethod
import pandas as pd
from immune_receptor_utils import utilities
import numpy as np

from pygmalion.bayesian_network_importer.conditional_matrix import ConditionalMatrix


class _EventProbabilities(object):
    _EVENT_TEXT_SEP = ';'

    def __init__(self, event_name, parents=None):
        self._items = {}
        self._parents = parents
        self._event_name = event_name

    def add_probabilites(self, row_id, probabilities):
        self._assert_structure(probabilities)
        self._items[row_id] = probabilities

    def get_row_ids(self):
        return self._items.keys()

    def _assert_structure(self, probabilities):
        keys = self._items.keys()
        if len(keys) > 0:
            self._assert_id_requirements(self._items.get(keys[0]), probabilities)

    def _assert_id_requirements(self, row1, row2):
        for i in range(len(row1)-1):
            v1 = row1[i]
            v1 = v1[0:len(v1) - 1]
            v2 = row2[i]
            v2 = v2[0:len(v2) - 1]
            if (_EventProbabilities._EVENT_TEXT_SEP in v1) or (_EventProbabilities._EVENT_TEXT_SEP in v2):
                raise AssertionError('Reserved separator character used in ids')
            if v1 != v2: raise AssertionError('Ids do not match')

    def get_as_dataframes(self, aggregate_on_gene_level=False):
        cols = self._get_df_columns_names()
        if cols is None: return None
        x, indices = self._get_df_data_and_indices(columns=cols, assert_keys=True)
        out = pd.DataFrame(data=x, columns=cols, index=indices)
        out = out.transpose()
        if aggregate_on_gene_level: out = self._aggregate_on_gene_level(out)
        return out

    def _get_df_columns_names(self):
        keys = self._items.keys()
        if len(keys) == 0: return None
        cols = []
        first_item = self._items.get(keys[0])
        for i in range(len(first_item)):
            col = first_item[i]
            col_id = self._get_df_column_name(col)
            cols.append(col_id)
        return cols

    def _get_df_column_name(self, col):
        col_id = ''
        for j in range(len(col) - 1):
            c = col[j]
            if len(col_id) > 0: col_id += _EventProbabilities._EVENT_TEXT_SEP
            col_id += c
        return col_id

    def _get_df_data_and_indices(self, columns, assert_keys=False):
        x = []
        indices = []
        for row_id, probabilities in self._items.iteritems():
            row = []
            indices.append(row_id)
            for i in range(len(probabilities)):
                # if assert_keys:
                #     tmp = self._get_df_column_name(probabilities[i])
                #     if self._assert_id_requirements(columns[i], tmp): raise AssertionError()
                p = probabilities[i][-1]
                row.append(p)
            x.append(row)
        return x, indices

    def _aggregate_on_gene_level(self, df):
        # if self._event_name not in ConditionalMatrix.GENE_NAME_NICKNAMES:
        #     raise AssertionError('Cannot aggregate on gene level for this nickname')
        df = self._create_row_ids_as_columns(df)
        groupby_cols = []
        if self._parents is None:
            if self._event_name in ConditionalMatrix.GENE_NAME_NICKNAMES:
                groupby_cols.append(self._event_name + '_gene')
        else:
            for p in self._parents:
                if p in ConditionalMatrix.GENE_NAME_NICKNAMES:
                    groupby_cols.append(p + '_gene')
                else:
                    groupby_cols.append(p)
        # df['allele'] = df.index
        # df['gene'] = df['allele'].str.extract('(.*)\*.*')
        agg_defs = {}
        for donor in self._items.keys():
            agg_defs[donor] = np.sum
        df = df.groupby(groupby_cols, as_index=False).agg(agg_defs)
        df['tmp_index'] = df[groupby_cols[0]]
        for i in range(1,len(groupby_cols)):
            g_col = groupby_cols[i]
            df['tmp_index'] += _EventProbabilities._EVENT_TEXT_SEP
            df['tmp_index'] += df[g_col]
        df.index = df['tmp_index']
        #df.index = df[groupby_cols[0]] + _EventProbabilities._EVENT_TEXT_SEP + df[groupby_cols[1]]
        df = df.drop('tmp_index', 1)
        for g in groupby_cols:
            df = df.drop(g, 1)
        # df.index = df['gene']
        # df = df.drop('gene', 1)
        return df

    def _create_row_ids_as_columns(self, df):
        df['row_id'] = df.index
        if self._parents is None:
            if self._event_name in ConditionalMatrix.GENE_NAME_NICKNAMES:
                df[self._event_name + '_gene'] = df['row_id'].str.extract('(.*)\*.*')
        else:
            new_df = df["row_id"].str.split(";", n=-1, expand=True)
            for i in range(len(self._parents)):
                p = self._parents[i]
                df[p] = new_df[i]
                if p in ConditionalMatrix.GENE_NAME_NICKNAMES:
                    df[p + '_gene'] = df[p].str.extract('(.*)\*.*')
        df = df.drop('row_id', 1)
        return df


class ProbabilitiesExporter(object):
    def __init__(self):
        self._items = {}

    def add_probabilities(self, row_id, event_name, probabilities, parents=None):
        dfs = self._items.get(event_name, None)
        if dfs is None:
            dfs = _EventProbabilities(event_name, parents)
            self._items[event_name] = dfs
        dfs.add_probabilites(row_id, probabilities)

    def get_as_dataframes(self, nicknames=None, aggregate_on_gene_level=False):
        self._assert_structure()
        if nicknames is None:
            nicknames = self._items.keys()
        dfs = []
        for nickname in nicknames:
            # agg = False
            # if aggregate_on_gene_level:
            #     if nickname in ConditionalMatrix.GENE_NAME_NICKNAMES: agg = True
            probabilities = self._items.get(nickname)
            df = probabilities.get_as_dataframes(aggregate_on_gene_level=aggregate_on_gene_level)
            dfs.append(df)
        out = pd.concat(dfs, axis=0, verify_integrity=True)
        return out

    def _assert_structure(self):
        template = None
        for key, value in self._items.iteritems():
            if template is None:
                template = value.get_row_ids()
            else:
                equal = self._row_ids_are_equal(template, value.get_row_ids())
                if not equal: raise AssertionError()

    def _row_ids_are_equal(self, row_ids1, row_ids2):
        if len(row_ids1) != len(row_ids2): return False
        for id in row_ids1:
            if id not in row_ids2: return False
        return True
