import collections


class Table(collections.MutableMapping):

    # mapping of this class to alphatwirl
    mapping = {
        'input_values': 'valAttrNames',
        'keyAttrNames': 'valAttrNames',
        'output_columns': 'valOutColumnNames',
        'indices': 'valIndices',
        'bins': 'binnings',
    }

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        new_key = self.__keytransform__(key)
        if new_key == 'valIndices' and new_key not in self.store:
            return [None] * len(self.store['valAttrNames'])
        return self.store[new_key]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        if key in Table.mapping:
            return Table.mapping[key]
        else:
            return key

    def copy(self):
        return Table(**self.store)

    def __repr__(self):
        result = []
        for k, v in self.store.items():
            result.append('{0}={1}'.format(k, v))
        title = '{}(): '.format(self.__class__.__name__)
        return title + ', '.join(result)

    @property
    def outputColumns(self):
        output = []
        if 'valOutColumnNames' in self.store:
            output.extend(self.store['valOutColumnNames'])
        if 'keyOutColumnNames' in self.store:
            output.extend(self.store['keyOutColumnNames'])
        # only return unique columns
        return list(set(output))
