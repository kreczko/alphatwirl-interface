from nose2.tools import such

from alphatwirl_interface.producers.invariantMass import _extract_index

with such.A('Invariant mass producer') as it:

    @it.should('extract index from branchname')
    def test_extract_indes():
        branchTemplate = 'Muon[{0}]'
        for i in [0, 4, 23, 999]:
            branch = branchTemplate.format(i)
            name, index = _extract_index(branch)
            it.assertEqual(name, 'Muon')
            it.assertEqual(index, i)
        name, index = _extract_index('Muon_1')
        it.assertEqual(name, 'Muon_1')
        it.assertEqual(index, None)


it.createTests(globals())
