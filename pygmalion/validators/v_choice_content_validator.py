from Logger import StdOutLogger
from pygmalion.donors.iterator import GenModelWrapperIterator
from pygmalion.genmodel.nicknames import Nicknames
from pygmalion.validators.validator import Validator


class VChoiceContentValidator(Validator):
    def __init__(self, logger=StdOutLogger(verbose=False)):
        super(VChoiceContentValidator, self).__init__(logger)

    def assert_validity(self, gen_model_wrappers):
        self._out = True
        itr = GenModelWrapperIterator(gen_model_wrappers)
        for gmw in itr:
            marginals = gmw.get_GenModel().marginals[0].get(Nicknames.v_choice.value)
            if len(marginals) == 0:
                raise AssertionError('No v_ choice content found for %s' % gmw.get_name())
            if not self._marginal_content_exist(marginals):
                raise AssertionError('No non-zero v_ choice content found for %s' % gmw.get_name())
        return self._out

    def _marginal_content_exist(self, marginals):
        for m in marginals:
            if m > 0.0: return True
        return False
