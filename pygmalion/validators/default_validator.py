from Logger import StdOutLogger
import immune_receptor_utils.enums as ir

from pygmalion.donors.iterator import GenModelWrapperIterator
from pygmalion.validators.v_choice_content_validator import VChoiceContentValidator
from pygmalion.validators.validator import Validator


class DefaultValidator(Validator):
    def __init__(self, logger=StdOutLogger(verbose=False)):
        super(DefaultValidator, self).__init__(logger)
        self._v_choice_content_validator = VChoiceContentValidator()
        self._out = None
        self._template = None

    def assert_validity(self, items):
        self._out = True
        for c in ir.Chain:
            self._template = None
            itr = GenModelWrapperIterator(items, filter_by_chain=c)
            for gmw in itr:
                if self._template is None:
                    self._template = gmw
                else:
                    self._template.assert_bayesian_network_structure_equality(gmw)
        self._v_choice_content_validator.assert_validity(items)
