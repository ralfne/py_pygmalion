from Logger import StdOutLogger


class GenModelWrappers(object):
    def __init__(self, logger=StdOutLogger(verbose=False)):
        self._logger = logger
        self._items = {}

    def add(self, genModelWrapper):
        if genModelWrapper.get_name() in self._items: raise ValueError('genModelWrapper name already in dict')
        self._items[genModelWrapper.get_name()] = genModelWrapper

    def __len__(self):
        return self._items.__len__()

    def __getitem__(self, k):
        return self._items.__getitem__(k)

    def __str__(self):
        out = ''
        for key, value in self._items.iteritems():
            out += str(value) + '\n'
        return out

    def keys(self):
        return self._items.keys()

    def iteritems(self):
        return self._items.iteritems()