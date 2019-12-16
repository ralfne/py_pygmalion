from pygmalion.donors.iterator import GenModelWrapperIterator, DonorIterator
from utils import *


def test_donors_1__test_rename(ced_donors):
    ced_donors.modify_names('donor_pre_', '_donor_post', 'gmw_pre_', '_gmw_post')
    itr = GenModelWrapperIterator(ced_donors)
    for gmw in itr:
        assert (gmw.get_name().startswith('gmw_pre_'))
        assert (gmw.get_name().endswith('_gmw_post'))
    itr = DonorIterator(ced_donors)
    for donor in itr:
        assert (donor.get_name().startswith('donor_pre_'))
        assert (donor.get_name().endswith('_donor_post'))