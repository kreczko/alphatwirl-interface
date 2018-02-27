import alphatwirl as at
from alphatwirl_interface import Table
from alphatwirl_interface.tree import _complement_tblcfg_with_default


def test_vanishing_attribute_names():
    '''
        Unit test for a bug: disappearing valAttrNames
    '''
    columns = ('NJet', 'di_muon_mass')
    tables = [
        Table(
            input_values=columns,
        ),
    ]

    default_cfg = dict(
        keyAttrNames=(),
        sort=False,
        summaryClass=at.summary.Scan,
        outFile=False,
    )
    tables = _complement_tblcfg_with_default(tables, default_cfg)
    assert tables[0]['valAttrNames'] == columns
