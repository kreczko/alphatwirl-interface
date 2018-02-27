import pytest
from alphatwirl_interface.producers.basic import BasicProducer

from .fixtures import example_event


@pytest.mark.usefixtures("example_event")
def test_basic_producer(example_event):
    e = example_event
    new_attr = 'testing'
    p = BasicProducer(
        new_attr,
    )
    # would usually be called in alphatwirl
    p.begin(e)
    p.event(e)
    assert hasattr(example_event, new_attr)
    assert getattr(e, new_attr)[0] == 42
