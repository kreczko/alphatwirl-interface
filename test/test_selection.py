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

def test_conversion_with_more_than_one():
    selection = Selection(
        dict(
            All=(
                'Muon_E[0] > 2 * Muon_Pt[1]',
                'Muon_Charge[0] == Muon_Charge[0]',
            )
        )
    )

    expected = dict(
        All=(
            'ev: ev.Muon_E[0] > 2 * ev.Muon_Pt[1]',
            'ev: ev.Muon_Charge[0] == ev.Muon_Charge[0]',
        )
    )

    assert_equals(selection._convert_to_alphatwirl(), expected)
