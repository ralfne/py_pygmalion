from bayesian_network_utilities.api.bayesian_network_wrapper import BayesianNetworkWrapper, ProbabilityType

from pygmalion.donors.iterator import GenModelWrapperIterator
from pygmalion.genmodel.gen_model_wrapper import GenModelWrapper
from pygmalion.genmodel.nicknames import Nicknames
from utils import *


def test_1__merge_tra_v_gene_alleles(merged_genmodelwrapper_1516_TRA):
    wrapper = merged_genmodelwrapper_1516_TRA.get_bayesian_network_wrapper()
    event = merged_genmodelwrapper_1516_TRA.get_event_from_nickname(Nicknames.v_choice.value)
    margs = wrapper.get_probabilities(event.name, probability_type=ProbabilityType.Marginal)
    assert (is_similar(margs.sum(), 1.0, 0.001))
    event = merged_genmodelwrapper_1516_TRA.get_event_from_nickname(Nicknames.j_choice.value)
    margs = wrapper.get_probabilities(event.name, probability_type=ProbabilityType.Marginal)
    assert (is_similar(margs.sum(), 1.0, 0.001))

def test_2__merge_trb_v_gene_alleles(merged_genmodelwrapper_1516_TRB):
    wrapper = merged_genmodelwrapper_1516_TRB.get_bayesian_network_wrapper()
    event = merged_genmodelwrapper_1516_TRB.get_event_from_nickname(Nicknames.v_choice.value)
    margs = wrapper.get_probabilities(event.name, probability_type=ProbabilityType.Marginal)
    assert (is_similar(margs.sum(), 1.0, 0.001))
    event = merged_genmodelwrapper_1516_TRB.get_event_from_nickname(Nicknames.j_choice.value)
    margs = wrapper.get_probabilities(event.name, probability_type=ProbabilityType.Marginal)
    assert (is_similar(margs.sum(), 1.0, 0.001))

def test_3__merge_alleles(ced_donors, hc_donors):
    itr = GenModelWrapperIterator(ced_donors, filter_by_chain=None)
    for gmw in itr:
        gmw.merge_alleles()
    itr = GenModelWrapperIterator(hc_donors, filter_by_chain=None)
    for gmw in itr:
        gmw.merge_alleles()
