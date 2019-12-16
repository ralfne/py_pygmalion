import ntpath
import os
from Logger import DummyLogger
import pytest
from pygmalion.donors.donors import Donors
from pygmalion.genmodel.gen_model_wrapper import GenModelWrapper
from pygmalion.persistence.default_persistence_handler import DefaultPersistenceHandler
from pygmalion.validators.default_validator import DefaultValidator

_TEST_DATA_DIRNAME = 'data'


def is_similar(value, target, delta):
    if value - delta > target: return False
    if value + delta < target: return False
    return True


def get_testdata_folder():
    out = os.path.realpath(__file__)
    out = ntpath.dirname(out)
    out = os.path.join(out, _TEST_DATA_DIRNAME)
    return out


def get_1516_TRA_marginals_and_params_filenames():
    data_folder = get_testdata_folder()
    fn_ced = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'CeD')
    fn_1516 = os.path.join(fn_ced, '1516_TRA')
    out_marginals = os.path.join(fn_1516, '1516_TRA_marginals.txt')
    out_params = os.path.join(fn_1516, '1516_TRA_params.txt')
    return out_marginals, out_params


def get_1516_TRB_marginals_and_params_filenames():
    data_folder = get_testdata_folder()
    fn_ced = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'CeD')
    fn_1516 = os.path.join(fn_ced, '1516_TRB')
    out_marginals = os.path.join(fn_1516, '1516_TRB_marginals.txt')
    out_params = os.path.join(fn_1516, '1516_TRB_params.txt')
    return out_marginals, out_params


@pytest.fixture
def genmodelwrapper_1516_TRA():
    fn_margs, fn_params = get_1516_TRA_marginals_and_params_filenames()
    gmw = GenModelWrapper(fn_params, fn_margs, '1516_TRA_', DummyLogger())
    return gmw

@pytest.fixture
def genmodelwrapper_1516_TRB():
    fn_margs, fn_params = get_1516_TRB_marginals_and_params_filenames()
    gmw = GenModelWrapper(fn_params, fn_margs, '1516_TRB_', DummyLogger())
    return gmw

@pytest.fixture
def merged_genmodelwrapper_1516_TRA():
    fn_margs, fn_params = get_1516_TRA_marginals_and_params_filenames()
    gmw = GenModelWrapper(fn_params, fn_margs, '1516_TRA_', DummyLogger())
    gmw.merge_alleles()
    return gmw

@pytest.fixture
def merged_genmodelwrapper_1516_TRB():
    fn_margs, fn_params = get_1516_TRB_marginals_and_params_filenames()
    gmw = GenModelWrapper(fn_params, fn_margs, '1516_TRB_', DummyLogger())
    gmw.merge_alleles()
    return gmw

@pytest.fixture
def ced_donors():
    persistence = DefaultPersistenceHandler(DummyLogger())
    data_folder = get_testdata_folder()
    fn_ced = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'CeD')
    out = persistence.instantiate(fn_ced, DummyLogger())
    return out

@pytest.fixture
def hc_donors():
    persistence = DefaultPersistenceHandler(DummyLogger())
    data_folder = get_testdata_folder()
    fn_hc = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'HC')
    out = persistence.instantiate(fn_hc, DummyLogger())
    return out
#
# @pytest.fixture
# def default_dataset():
#     data_folder = get_testdata_folder()
#     fn_healthy = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'HC')
#     fn_ced = os.path.join(data_folder, 'models_imgt_ref_dir_sep2019', 'CeD')
#     out = GroupsDataset()
#     items = DefaultPersistenceHandler.instantiate(fn_healthy, DummyLogger())
#     validator = DefaultValidator()
#     validator.run(items)
#     out.add_data('HC', items)
#     items = DefaultPersistenceHandler.instantiate(fn_ced, DummyLogger())
#     validator.run(items)
#     out.add_data('CeD', items)
#     return out
