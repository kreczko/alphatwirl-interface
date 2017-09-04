import numpy as np

from .basic import BasicProducer


class NewFromFunction(BasicProducer):

    def __init__(self, outputName, inputs, function):
        super(NewFromFunction, self).__init__(outputName)
        self.inputs = inputs
        self.function = function

    def _value(self, obj):
        return self.function(
            *[np.array(getattr(obj, n)) for n in self.inputs]
        )

    def __repr__(self):
        attributes = ['outputName', 'inputs', 'function']
        formattedAttrs = super(
            NewFromFunction, self)._format_attributes(attributes)

        return '{}({})'.format(
            self.__class__.__name__,
            formattedAttrs,
        )


class Divide(NewFromFunction):
    def __init__(self, outputName, inputs):
        super(self.__class__, self).__init__(outputName, inputs, np.divide)

class TransverseMomentum(NewFromFunction):
    def __init__(self, outputName, inputs):
        super(self.__class__, self).__init__(
            outputName,
            inputs,
            function = lambda x, y: np.sqrt(np.square(x) + np.square(y))
        )
