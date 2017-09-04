import numpy as np
import re
from .basic import BasicProducer


def _extract_index(name):
    token = '\[\d+\]'
    match = re.search(token, name)
    if match:
        substr = match.group(0)
        index = int(substr.strip('[]'))
        newName = name.replace(substr, '')

        return newName, index
    return name, None

def _extract_values(obj, namesAndIndices):
    for (name, index) in namesAndIndices:
        if index is not None:
            yield getattr(obj, name)[index]
        else:
            yield getattr(obj, name)

class InvariantMass(BasicProducer):

    def __init__(self, outputName, fourMomentum1, fourMomentum2):
        '''
            fourMomentum = [energy, px, py, pz]
        '''
        super(InvariantMass, self).__init__(outputName)
        self.input1 = [_extract_index(x) for x in fourMomentum1]
        self.input2 = [_extract_index(x) for x in fourMomentum2]

        self.v1 = []
        self.v2 = []

    def _value(self, obj):
        self.v1[:] = list(_extract_values(obj, self.input1))
        self.v2[:] = list(_extract_values(obj, self.input2))

        energy = self.v1[0] * self.v2[0]
        momentum = np.dot(self.v1[1:], self.v2[1:])
        return [np.sqrt(energy - momentum)]
