class _IndexNameGuide(object):
    def __init__(self, index, name_or_value, extract_gene_id_from_name=False):
        self.index = index
        self.name_or_value = name_or_value
        if extract_gene_id_from_name: self._possibly_extract_gene_name()

    def _possibly_extract_gene_name(self):
        if '|' in self.name_or_value:
            i1 = self.name_or_value.index('TR')
            i2 = self.name_or_value.index('*')
            s = self.name_or_value[i1:i2 + 3]
            self.name_or_value = s

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, _IndexNameGuide): return False
        if self.index != other.index: return False
        if isinstance(self.name_or_value, basestring):
            if self.name_or_value.strip() != other.name_or_value.strip(): return False
        else:
            if self.name_or_value != other.name_or_value: return False
        return True


class _IndexNameGuideList(object):
    def __init__(self, event, event_uses_gene_names=False):
        tmp = []
        realizations = event.realizations
        for i in range(len(realizations)):
            r = realizations[i]
            if r.name == '':
                name = r.value
            else:
                name = r.name
            guide = _IndexNameGuide(r.index, name, event_uses_gene_names)
            tmp.append(guide)
        self.items = sorted(tmp, key=lambda x: x.index)

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return self.items.__len__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        if not isinstance(other, _IndexNameGuideList): return False
        for i in range(len(self.items)):
            my_item = self.items[i]
            other_item = other[i]
            if not my_item == other_item: return False
        return True
