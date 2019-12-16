from pygmalion.donors.donor import Donor
from pygmalion.donors.iterator import GenModelWrapperIterator, DonorIterator
from pygmalion.genmodel.gen_model_wrappers import GenModelWrappers
from utils import *
import immune_receptor_utils.enums as ir


def test_iterator_1__test_donors(ced_donors):
    itr = GenModelWrapperIterator(ced_donors, filter_by_chain=None)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        count += 1
    assert count == 22

def test_iterator_2__test_donors(ced_donors):
    itr = DonorIterator(ced_donors)
    count = 0
    for item in itr:
        assert (isinstance(item, Donor))
        count += 1
    assert count == 11

def test_iterator_3__test_donors(ced_donors):
    itr = GenModelWrapperIterator(ced_donors, filter_by_chain=ir.Chain.TRB)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        assert ('TRB' in item.get_name())
        count += 1
    assert count == 11

def test_iterator_5__test_genmodelwrappers(ced_donors):
    gmws = GenModelWrappers()
    for key, donor in ced_donors.iteritems():
        gmws.add(donor.get_genmodel_wrapper(ir.Chain.TRA))
        gmws.add(donor.get_genmodel_wrapper(ir.Chain.TRB))
    itr = GenModelWrapperIterator(gmws, filter_by_chain=None)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        count += 1
    assert count == 22

def test_iterator_6__test_genmodelwrappers(ced_donors):
    gmws = GenModelWrappers()
    for key, donor in ced_donors.iteritems():
        gmws.add(donor.get_genmodel_wrapper(ir.Chain.TRA))
        gmws.add(donor.get_genmodel_wrapper(ir.Chain.TRB))
    itr = DonorIterator(gmws)
    count = 0
    for item in itr:
        count += 1
    assert count == 0

def test_iterator_7__test_genmodelwrappers(ced_donors):
    gmws = GenModelWrappers()
    for key, donor in ced_donors.iteritems():
        gmws.add(donor.get_genmodel_wrapper(ir.Chain.TRA))
        gmws.add(donor.get_genmodel_wrapper(ir.Chain.TRB))
    itr = GenModelWrapperIterator(gmws, filter_by_chain=ir.Chain.TRB)
    count = 0
    for item in itr:
        count += 1
    assert count == 0

def test_iterator_9__test_donorlist(ced_donors):
    lst = []
    for key, donor in ced_donors.iteritems():
        lst.append(donor)
    itr = GenModelWrapperIterator(lst, filter_by_chain=None)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        count += 1
    assert count == 22

def test_iterator_10__test_donorlist(ced_donors):
    lst = []
    for key, donor in ced_donors.iteritems():
        lst.append(donor)
    itr = DonorIterator(lst)
    count = 0
    for item in itr:
        assert (isinstance(item, Donor))
        count += 1
    assert count == 11

def test_iterator_11__test_donorlist(ced_donors):
    lst = []
    for key, donor in ced_donors.iteritems():
        lst.append(donor)
    itr = GenModelWrapperIterator(lst, filter_by_chain=ir.Chain.TRB)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        assert ('TRB' in item.get_name())
        count += 1
    assert count == 11

def test_iterator_13__test_donordict(ced_donors):
    dct = {}
    for key, donor in ced_donors.iteritems():
        dct[key] = donor
    itr = GenModelWrapperIterator(dct, filter_by_chain=None)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        count += 1
    assert count == 22

def test_iterator_14__test_donordict(ced_donors):
    dct = {}
    for key, donor in ced_donors.iteritems():
        dct[key] = donor
    itr = DonorIterator(dct)
    count = 0
    for item in itr:
        assert (isinstance(item, Donor))
        count += 1
    assert count == 11

def test_iterator_15__test_donordict(ced_donors):
    dct = {}
    for key, donor in ced_donors.iteritems():
        dct[key] = donor
    itr = GenModelWrapperIterator(dct, filter_by_chain=ir.Chain.TRB)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        assert ('TRB' in item.get_name())
        count += 1
    assert count == 11

def test_iterator_15__test_mixedlist(ced_donors):
    lst = []
    lst.append(ced_donors.get_donor_from_index(3))
    lst.append(ced_donors.get_donor_from_index(1))
    gmw = ced_donors.get_donor_from_index(5).get_genmodel_wrapper(ir.Chain.TRB)
    lst.append(gmw)
    lst.append(ced_donors.get_donor_from_index(5))
    gmw = ced_donors.get_donor_from_index(4).get_genmodel_wrapper(ir.Chain.TRA)
    lst.append(gmw)
    itr = DonorIterator(lst)
    count = 0
    for item in itr:
        assert (isinstance(item, Donor))
        count += 1
    assert (count == 3)
    itr = GenModelWrapperIterator(lst)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        count += 1
    assert (count == 8)
    itr = GenModelWrapperIterator(lst, filter_by_chain=ir.Chain.TRA)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        assert ('TRA' in item.get_name())
        count += 1
    assert (count == 3)
    itr = GenModelWrapperIterator(lst, filter_by_chain=ir.Chain.TRB)
    count = 0
    for item in itr:
        assert (isinstance(item, GenModelWrapper))
        assert ('TRB' in item.get_name())
        count += 1
    assert (count == 3)