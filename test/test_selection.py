from alphatwirl_interface import Selection
from nose.tools import assert_equals


def test_conversion():
    selection = Selection(
        dict(
            All=(
                'NMuon == 2',
                dict(
                    Any=(
                        'NJet == 2',
                        'NJet == 3',
                    )
                )
            )
        )
    )

    expected = dict(
        All=(
            'ev: ev.NMuon == 2',
            dict(
                Any=(
                    'ev: ev.NJet == 2',
                    'ev: ev.NJet == 3',
                )
            )
        )
    )

    assert_equals(selection._convert_to_alphatwirl(), expected)
