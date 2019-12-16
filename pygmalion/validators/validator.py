from abc import ABCMeta, abstractmethod

from Logger import StdOutLogger


class Validator(object):
    __metaclass__ = ABCMeta

    def __init__(self, logger=StdOutLogger(verbose=False)):
        self._logger = logger

    @abstractmethod
    def assert_validity(self, genModelWrappers): pass

