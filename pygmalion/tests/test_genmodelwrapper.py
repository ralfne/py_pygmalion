from pygmalion.donors.iterator import Iterator, GenModelWrapperIterator
from pygmalion.genmodel.gen_model_wrapper import GenModelWrapper
import immune_receptor_utils.enums as ir
from utils import *


def test_1__load_tra_genmodelwrapper():
    fn_margs, fn_params  = get_1516_TRA_marginals_and_params_filenames()
    gmw = GenModelWrapper(fn_params, fn_margs, '1516_TRA_', DummyLogger())
    assert (gmw is not None)

def test_2__load_trb_genmodelwrapper():
    fn_margs, fn_params = get_1516_TRB_marginals_and_params_filenames()
    gmw = GenModelWrapper(fn_params, fn_margs, '1516_TRB_', DummyLogger())
    assert (gmw is not None)

def test_3__assert_structure_tra_vs_tra(merged_genmodelwrapper_1516_TRA):
    merged_genmodelwrapper_1516_TRA.assert_bayesian_network_structure_equality(merged_genmodelwrapper_1516_TRA)

def test_4__assert_structure_tra_vs_trb(merged_genmodelwrapper_1516_TRA, merged_genmodelwrapper_1516_TRB):
    with pytest.raises(Exception) as e:
        assert  merged_genmodelwrapper_1516_TRA.assert_bayesian_network_structure_equality(merged_genmodelwrapper_1516_TRB)
    assert (str(e.value) == '1516_TRA_vs. 1516_TRB_: Number of states not equal')

def test_5__check_marginals_agains_primitives(ced_donors):
    itr = GenModelWrapperIterator(ced_donors,filtering_chain=ir.Chain.TRB)
    for gmw in itr:
        m = gmw._get_v_gene_marginal_from_primitives('TRBV7-2*01')
        x= m
    #assert (m>0)

