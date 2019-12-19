from __builtin__ import object
from abc import ABCMeta, abstractmethod
import immune_receptor_utils.enums as ir
from pygmalion.donors.donor import Donor
from pygmalion.donors.donors import Donors
from pygmalion.genmodel.gen_model_wrapper import GenModelWrapper
from pygmalion.genmodel.gen_model_wrappers import GenModelWrappers


class Iterator(object):
    __metaclass__ = ABCMeta

    def __init__(self, items, filtering_chain=None):
        if not(isinstance(items, dict) or isinstance(items, Donors) or
                            isinstance(items, GenModelWrappers) or
                            isinstance(items, list) or
                            isinstance(items, Donor) or
                            isinstance(items, GenModelWrapper)):
            raise NotImplementedError()
        self._items = []
        self._add_item_for_object(items, self._items, filtering_chain)

    @abstractmethod
    def _add_items_for_genmodelwrapper(self, genmodelwrapper, items, filtering_chain):
        pass

    @abstractmethod
    def _add_items_for_donor(self, donor, items, filtering_chain):
        pass

    def _add_items_for_genmodelwrappers(self, genmodelwrappers, items, filtering_chain):
        for key, gmw in genmodelwrappers.iteritems():
            self._add_items_for_genmodelwrapper(gmw, items, filtering_chain)

    def _add_items_for_donors(self, donors, items, filtering_chain):
        for key, donor in donors.iteritems():
            self._add_items_for_donor(donor, items, filtering_chain)

    def _add_item_for_object(self, obj, items, filtering_chain):
        if isinstance(obj, GenModelWrapper):
            self._add_items_for_genmodelwrapper(obj, items, filtering_chain)
        elif isinstance(obj, GenModelWrappers):
            self._add_items_for_genmodelwrappers(obj, items, filtering_chain)
        elif isinstance(obj, Donor):
            self._add_items_for_donor(obj, items, filtering_chain)
        elif isinstance(obj, Donors):
            self._add_items_for_donors(obj, items, filtering_chain)
        elif isinstance(obj, list):
            self._add_items_for_list(obj, items, filtering_chain)
        elif isinstance(obj, dict):
            self._add_items_for_dict(obj, items, filtering_chain)
        else:
            raise NotImplementedError()

    def _add_items_for_list(self, lst, items, filtering_chain):
        for item in lst:
            self._add_item_for_object(item, items, filtering_chain)

    def _add_items_for_dict(self, dct, items, filtering_chain):
        for key, item in dct.iteritems():
            self._add_item_for_object(item, items, filtering_chain)

    def __iter__(self):
        return self._items.__iter__()

    def next(self):
        self._index += 1
        if self._index <= len(self._items):
            return self._index
        raise StopIteration


class GenModelWrapperIterator(Iterator):
    def __init__(self, items, filtering_chain=None):
        super(GenModelWrapperIterator, self).__init__(items, filtering_chain)

    def _add_items_for_genmodelwrapper(self, genmodelwrapper, items, filtering_chain):
            if filtering_chain is None:
                items.append(genmodelwrapper)

    def _add_items_for_donor(self, donor, items, filtering_chain):
        for c in ir.Chain:
            gmw = donor.get_genmodel_wrapper(c)
            if gmw is not None:
                if (filtering_chain is None) or (c == filtering_chain):
                    items.append(gmw)


class DonorIterator(Iterator):
    def __init__(self, items):
        super(DonorIterator, self).__init__(items, filtering_chain=None)

    def _add_items_for_genmodelwrapper(self, genmodelwrapper, items, filtering_chain):
        pass

    def _add_items_for_donor(self, donor, items, filtering_chain):
        items.append(donor)
