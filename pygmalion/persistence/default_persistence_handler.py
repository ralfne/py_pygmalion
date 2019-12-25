import os
from Logger import StdOutLogger
import ntpath
from immune_receptor_utils import enums as ir
from pygmalion.donors.donor import Donor
from pygmalion.donors.donors import Donors
from pygmalion.persistence.persistence_handler import PersistenceHandler


class DonorFilenames(object):
    _MARGINALS_TEXT = 'marginals'
    _PARAMS_TEXT = 'params'
    _TRA_TEXT = 'TRA'
    _TRB_TEXT = 'TRB'

    def __init__(self):
        self._params_fns = {}
        self._marginals_fns = {}

    def add_params_fn(self, fn, ir_chain):
        self._params_fns[ir_chain] = fn

    def get_params_fn(self, ir_chain):
        return self._params_fns.get(ir_chain, None)

    def add_marginals_fn(self, fn, ir_chain):
        self._marginals_fns[ir_chain] = fn

    def get_marginals_fn(self, ir_chain):
        return self._marginals_fns.get(ir_chain, None)


class _FilenamesBroker(object):
    def __init__(self, filenames=None):
        self._ids = {}
        if filenames is not None: self._init_from_files(filenames)

    def __len__(self):
        return self._ids.__len__()

    def __iter__(self):
        return self._ids.__iter__()

    def iteritems(self):
        return self._ids.iteritems()

    def extend(self, cells_filenames):
        for name, value in cells_filenames.iteritems():
            if self._ids.__contains__(name): raise ValueError('Name already in use')
            self._ids[name] = cells_filenames

    def _init_from_files(self, filenames):
        for fn in filenames:
            self._potentially_add_cell_id(fn)

    def validate(self):
        for name, value in self._ids.iteritems():
            if not(value.get_marginals_fn(ir.Chain.TRA) and (value.get_params_fn(ir.Chain.TRA)) and
                   (value.get_marginals_fn(ir.Chain.TRB)) and (value.get_params_fn(ir.Chain.TRB))):
                return False
        return True

    def _potentially_add_cell_id(self, path):
        head, tail = ntpath.split(path)
        fn = tail or ntpath.basename(head)
        is_tra = True
        chain_index = fn.find(DonorFilenames._TRA_TEXT)
        if chain_index == -1:
            chain_index = fn.find(DonorFilenames._TRB_TEXT)
            is_tra = False
        is_marginals = True
        type_index = fn.find(DonorFilenames._MARGINALS_TEXT)
        if type_index == -1:
            type_index = fn.find(DonorFilenames._PARAMS_TEXT)
            is_marginals = False
        if (chain_index == -1) or (type_index == -1): return None
        if chain_index < type_index: index = chain_index
        else: index = type_index
        id_string = fn[0:index]
        out = self._ids.get(id_string, None)
        if out is None:
            out = DonorFilenames()
            self._ids[id_string] = out
        if is_tra:
            if is_marginals: out.add_marginals_fn(path, ir.Chain.TRA)
            else: out.add_params_fn(path, ir.Chain.TRA)
        else:
            if is_marginals: out.add_marginals_fn(path, ir.Chain.TRB)
            else: out.add_params_fn(path, ir.Chain.TRB)


class DefaultPersistenceHandler(PersistenceHandler):
    def __init__(self, logger=StdOutLogger(verbose=False)):
        super(DefaultPersistenceHandler, self).__init__(logger)

    @staticmethod
    def instantiate(foldername, logger=StdOutLogger(verbose=False)):
        broker = DefaultPersistenceHandler._get_filenames_broker(foldername)
        out = DefaultPersistenceHandler._load_cells_from_filename_broker(broker, logger)
        logger.log('Donors loaded from folder ' + foldername, includeTimestamp=True, onlyIfVerbose=False)
        return out

    @staticmethod
    def _get_filenames_broker(foldername):
        folder_filenames = []
        for r, d, f in os.walk(foldername):
            for fn in f:
                full_fn = os.path.join(r, fn)
                folder_filenames.append(full_fn)
        out = _FilenamesBroker(folder_filenames)
        if not out.validate(): raise ValueError('PairedIgorModelFnsDict not valid')
        return out

    @staticmethod
    def _load_cells_from_filename_broker(broker, logger):
        out = Donors(logger)
        for cellname, cell_files in broker.iteritems():
            logger.log('Loading models for %s ...' % cellname, False, True)
            donor = Donor(cell_files, cellname, logger)
            out.add_donor(donor)
            for chain in ir.Chain:
                gmw = donor.get_genmodel_wrapper(chain)
                if gmw is not None:
                    params_fn = cell_files.get_params_fn(chain)
                    marginals_fn = cell_files.get_marginals_fn(chain)
                    name = DefaultPersistenceHandler._get_genmodel_wrapper_name(params_fn, marginals_fn)
                    gmw.set_name(name)
        return out

    @staticmethod
    def _get_genmodel_wrapper_name(params_fn, marginal_fn):
        fn1 = os.path.basename(params_fn)
        fn2 = os.path.basename(marginal_fn)
        filename, file_extension = os.path.splitext(fn1)
        fn1 = fn1.replace(file_extension, '')
        filename, file_extension = os.path.splitext(fn2)
        fn2 = fn2.replace(file_extension, '')
        cut_index = -1
        for i in range(len(fn1)):
            if fn1[i] != fn2[i]:
                cut_index = i
                break
        if cut_index == -1:
            out = fn1
        else:
            out = fn1[0: cut_index]
        return out
