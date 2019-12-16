import os

from Logger import StdOutLogger

from pygmalion.donors.iterator import GenModelWrapperIterator
from pygmalion.genmodel.gen_model_wrapper import GenModelWrapper
from pygmalion.persistence.default_persistence_handler import DefaultPersistenceHandler
from pygmalion.persistence.pickle_persistence_handler import PicklePersistenceHandler
from pygmalion.tests.utils import get_testdata_folder

# persistence = DefaultPersistenceHandler(StdOutLogger())
# data_folder = get_testdata_folder()
# fn_ced = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'CeD')
# ced_donors = persistence.instantiate(fn_ced, StdOutLogger())
#



data_folder = get_testdata_folder()
fn_ced = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'CeD')
fn_1516 = os.path.join(fn_ced, '1424_TRB')
out_marginals = os.path.join(fn_1516, '1424_TRB_marginals.txt')
out_params = os.path.join(fn_1516, '1424_TRB_params.txt')

gmw = GenModelWrapper(out_params, out_marginals, '1424_TRB_', StdOutLogger())
gmw.merge_alleles()

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