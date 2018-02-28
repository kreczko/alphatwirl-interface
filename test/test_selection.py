import pytest

from alphatwirl_interface import Selection
from alphatwirl.selection.modules import AllwCount
from alphatwirl.loop import Collector, NullCollector
from alphatwirl.collector import WriteListToFile


@pytest.fixture
def example_selection():
    selection = Selection(
        dict(
            All=(
                'di_muon_mass[0] > 60',
                'di_muon_mass[0] < 120',
            )
        )
    )
    return selection


def test_cutflow_file(example_selection):
    s = example_selection
    s.set_cutflow_file('/tmp/test.txt')
    s_tuple = s.as_tuple()
    assert len(s_tuple) == 2
    assert isinstance(s_tuple[0], AllwCount)
    assert isinstance(s_tuple[1], Collector)
    assert isinstance(s_tuple[1].deliveryMethod, WriteListToFile)


def test_no_cutflow_file(example_selection):
    s = example_selection
    s_tuple = s.as_tuple()
    assert len(s_tuple) == 2
    assert isinstance(s_tuple[0], AllwCount)
    assert isinstance(s_tuple[1], NullCollector)
