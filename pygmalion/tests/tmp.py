import os
import pomegranate as pom
from Logger import StdOutLogger
from bayesian_network_utilities.api.bayesian_network_wrapper import BayesianNetworkWrapper
from bayesian_network_utilities.api.distribution_event_merge_definitions import DistributionEventMergeDefinitions
from bayesian_network_utilities.api.event_merge_definition import EventMergeDefinition

from pygmalion.donors.iterator import GenModelWrapperIterator
from pygmalion.genmodel.gen_model_wrapper import GenModelWrapper
from pygmalion.persistence.default_persistence_handler import DefaultPersistenceHandler
from pygmalion.tests.utils import get_testdata_folder

# persistence = DefaultPersistenceHandler(StdOutLogger())
# data_folder = get_testdata_folder()
# fn_ced = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'CeD')
# ced_donors = persistence.instantiate(fn_ced, StdOutLogger())
#

def create_truncated_network(template):
    template_wrapper = BayesianNetworkWrapper(template)
    out = pom.BayesianNetwork()
    v_state = template_wrapper.get_state('GeneChoice_V_gene_Undefined_side_prio7_size147')
    #v_del_state = template_wrapper.get_state('Deletion_V_gene_Three_prime_prio5_size21')
    j_state = template_wrapper.get_state('GeneChoice_J_gene_Undefined_side_prio7_size16')
    #j_del_state = template_wrapper.get_state('Deletion_J_gene_Five_prime_prio5_size23')
    d_state = template_wrapper.get_state('GeneChoice_D_gene_Undefined_side_prio6_size3')
    out.add_states(v_state, j_state, d_state)
    #out.add_states(v_state, j_state, v_del_state, j_del_state, d_state)
    out.add_edge(v_state, j_state)
    #out.add_edge(v_state, v_del_state)
    #out.add_edge(j_state, j_del_state)
    out.add_edge(v_state, d_state)
    out.add_edge(j_state, d_state)
    out.bake()
    return out

def create_merg_defs(bn):
    merge_def1 = EventMergeDefinition('v_choice:TRBV7-2')
    merge_def1.extend(['v_choice:TRBV7-2*01', 'v_choice:TRBV7-2*02', 'v_choice:TRBV7-2*03', 'v_choice:TRBV7-2*04'])
    merge_defs = DistributionEventMergeDefinitions('GeneChoice_V_gene_Undefined_side_prio7_size147', bn,
                                                   allow_unspecified_events=True,
                                                   assert_merge_definitions=True)
    merge_defs.set_merge_definitions([merge_def1])
    return merge_defs


data_folder = get_testdata_folder()
fn_ced = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'HC')
fn_1363 = os.path.join(fn_ced, '1363_TRB')
out_marginals = os.path.join(fn_1363, '1363_TRB_marginals.txt')
out_params = os.path.join(fn_1363, '1363_TRB_params.txt')
print out_marginals
print out_params

out_marginals = 'C:/CiR/pTCR/IGOR_models/Unproductive_models/models_imgt_ref_dir_sep2019/HC/1365_TRB/1365_TRB_marginals.txt'
out_params = 'C:/CiR/pTCR/IGOR_models/Unproductive_models/models_imgt_ref_dir_sep2019/HC/1365_TRB/1365_TRB_params.txt'

gmw = GenModelWrapper(out_params, out_marginals, '1363_TRB_', StdOutLogger())
gmw.merge_alleles(assert_merge_definitions=True)
bn = gmw.get_bayesian_network_wrapper().get_network()



# truncate_bn = create_truncated_network(bn)
# truncate_bn_wrapper = BayesianNetworkWrapper(truncate_bn)
merge_defs = create_merg_defs(bn)
merged_bayesian_network = gmw.get_bayesian_network_wrapper().create_network_with_merged_events(merge_defs, bake=False)
merged_bayesian_network.bake()










bnwrapper = BayesianNetworkWrapper(merged_bayesian_network)
states = {}
n = gmw.get_eventname_for_nickname('v_choice')
state = bnwrapper.get_state(n)
states[n] = state

n = gmw.get_eventname_for_nickname('j_choice')
state = bnwrapper.get_state(n)
states[n] = state

n = gmw.get_eventname_for_nickname('d_gene')
state = bnwrapper.get_state(n)
states[n] = state

n = gmw.get_eventname_for_nickname('v_del3')
state = bnwrapper.get_state(n)
states[n] = state
merged_bayesian_network.bake()

#gmw.merge_alleles( assert_merge_definitions=True)
print 2

# persistence = DefaultPersistenceHandler(StdOutLogger())
# data_folder = get_testdata_folder()
# fn_hc = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'HC')
# hc_donors = persistence.instantiate(fn_hc, StdOutLogger())
#
# gmw = ced_donors.get_donor('1424_TRB_')
# gmw.merge_alleles()
#
# itr = GenModelWrapperIterator(ced_donors, filter_by_chain=None)
# for gmw in itr:
#     print ':::' + gmw.get_name()
#     gmw.merge_alleles()
#
# itr = GenModelWrapperIterator(hc_donors, filter_by_chain=None)
# for gmw in itr:
#     print ':::' + gmw.get_name()
#     gmw.merge_alleles()


#
# :::1424_TRB_
# 2019-12-16 00:09:03.053000: Merging...
# Merging 'v_choice:TRBV23/OR9-2' (66 of 66)2019-12-16 00:09:23.397000: Merging done!
# 2019-12-16 00:09:23.399000: Merging...
# Merging 'j_choice:TRBJ1-1' (14 of 14)2019-12-16 00:09:24.838000: Merging done!
# 2019-12-16 00:09:24.841000: Merging...
# Merging 'd_gene: TRBD2' (1 of