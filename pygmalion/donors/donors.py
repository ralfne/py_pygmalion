from Logger import StdOutLogger
from pygmalion.genmodel.gen_model_wrappers import GenModelWrappers
import immune_receptor_utils.enums as ir


class Donors(object):
    def __init__(self, logger=StdOutLogger(False)):
        self._items = {}
        self._models = GenModelWrappers(logger)
        self._logger = logger

    def add_donor(self, donor):
        if donor.get_name() in self._items: raise ValueError('Donor name already used in donors dict')
        self._items[donor.get_name()] = donor
        for c in donor.get_chains():
            self._models.add(donor.get_genmodel_wrapper(c))

    def get_donor_names(self):
        return self._items.keys()

    def iteritems(self):
        return self._items.iteritems()

    def __getitem__(self, k):
        return self._items.__getitem__(k)

    def __len__(self):
        return self._items.__len__()

    def __str__(self):
        out = ''
        for key, value in self._items.iteritems():
            out += str(value) + '\n'
        return out

    def get_donor_from_index(self, i):
        k = self._items.keys()[i]
        return self._items.get(k)

    def get_donor(self, name):
        return self._items.get(name)

    def delete_donor(self, name):
        del self._items[name]

    def get_model(self, name):
        return self._models[name]

    def get_models(self):
        return self._models

    def modify_names(self, donor_prefix='', donor_postfix='', genmodel_wrapper_prefix='', genmodel_wrapper_postfix=''):
        if (genmodel_wrapper_prefix != '') or (genmodel_wrapper_postfix != ''):
            for key, donor in self.iteritems():
                for c in ir.Chain:
                    gmw = donor.get_genmodel_wrapper(c)
                    if gmw is not None:
                        name = genmodel_wrapper_prefix + gmw.get_name() + genmodel_wrapper_postfix
                        gmw.set_name(name)
        if (donor_prefix != '') or (donor_postfix != ''):
            for key, donor in self.iteritems():
                name = donor_prefix + donor.get_name() + donor_postfix
                donor.set_name(name)
