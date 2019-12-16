from abc import ABCMeta, abstractmethod


class PersistenceHandler(object):
    __metaclass__ = ABCMeta

    def __init__(self, logger):
        self._logger = logger

    @staticmethod
    def instantiate(foldername, logger): pass
