from collections import namedtuple
import pytest
import numpy as np
from alphatwirl_interface.producers.invariantMass import _extract_index, _extract_values
from alphatwirl_interface.producers import InvariantMass


@pytest.fixture
def example_event():
    class Event(object):
        def __init__(self, Muon_E, Muon_Px, Muon_Py, Muon_Pz):
            self.Muon_E = Muon_E
            self.Muon_Px = Muon_Px
            self.Muon_Py = Muon_Py
            self.Muon_Pz = Muon_Pz
    # Event = namedtuple(
    #     'Event', ['Muon_E', 'Muon_Px', 'Muon_Py', 'Muon_Pz'])
    event = Event(
        Muon_E=[50, 60],
        Muon_Px=[10, 10],
        Muon_Py=[20, 30],
        Muon_Pz=[20, 20],
    )
    return event


@pytest.mark.parametrize("test_input,expected_name,expected_index", [
    ('Muon[0]', 'Muon', 0),
    ('Muon[4]', 'Muon', 4),
    ('Muon[23]', 'Muon', 23),
    ('Muon[999]', 'Muon', 999),
    ('Muon_1', 'Muon_1', None),
])
def test_extract_index(test_input, expected_name, expected_index):
    name, index = _extract_index(test_input)
    assert name == expected_name
    assert index == expected_index


def test_extract_values(example_event):
    namesAndIndices = [('Muon_E', 1), ('Muon_Pz', 0)]
    values = list(_extract_values(example_event, namesAndIndices))
    assert values[0] == example_event.Muon_E[1]
    assert values[1] == example_event.Muon_Pz[0]


def test_invariant_mass(example_event):
    di_muon_mass = InvariantMass(
        'di_muon_mass',
        ['Muon_E[0]', 'Muon_Px[0]', 'Muon_Py[0]', 'Muon_Pz[0]'],
        ['Muon_E[1]', 'Muon_Px[1]', 'Muon_Py[1]', 'Muon_Pz[1]'],
    )
    # would usually be called in alphatwirl
    di_muon_mass.begin(example_event)
    di_muon_mass.event(example_event)
    # manual calculation
    v0 = [example_event.Muon_E[0], example_event.Muon_Px[0],
          example_event.Muon_Py[0], example_event.Muon_Pz[0]]
    v1 = [example_event.Muon_E[1], example_event.Muon_Px[1],
          example_event.Muon_Py[1], example_event.Muon_Pz[1]]
    v = np.add(v0, v1)
    energySquared = pow(v[0], 2)
    momentumSquared = np.dot(v[1:], v[1:])
    expected_mass = np.sqrt(energySquared - momentumSquared)
    # test
    assert hasattr(example_event, 'di_muon_mass')
    assert getattr(example_event, 'di_muon_mass') == expected_mass
