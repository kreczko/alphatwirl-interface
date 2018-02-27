from collections import namedtuple
import pytest
import numpy as np
from alphatwirl_interface.producers import TransverseMomentum

from .fixtures import example_event


@pytest.mark.usefixtures("example_event")
def test_transverse_momentum(example_event):
    e = example_event
    pT = TransverseMomentum(
        'muon_pt',
        inputs=['Muon_Px', 'Muon_Py'],
    )
    # would usually be called in alphatwirl
    pT.begin(example_event)
    pT.event(example_event)
    # manual calculation
    expected_pt = np.sqrt(np.square(e.Muon_Px) + np.square(e.Muon_Py))
    # test
    assert hasattr(example_event, 'muon_pt')
    for mu_pt, exp_pt in zip(getattr(e, 'muon_pt'), expected_pt):
        assert mu_pt == exp_pt
