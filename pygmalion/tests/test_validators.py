from pygmalion.validators.default_validator import DefaultValidator
from utils import *


def test_validators_1__default_validator(ced_donors):
    validator = DefaultValidator()
    validator.assert_validity(ced_donors)
