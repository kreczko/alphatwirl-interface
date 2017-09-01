'''
In:
    Selection.append('NMuon == 2')
    Selection.append(['NJet == 2', 'NJet == 3'], require=Selection.Any)

Out:
    event_selection = dict(
        All = (
            'ev : ev.NMuon == 2',
            Any = (
                'ev : ev.NJet == 2',
                'ev : ev.NJet == 3',
            )
        )
    )
'''
from collections import Sequence
from alphatwirl_interface.cut_flows import cut_flow, cut_flow_with_counter
import six


class Selection(object):

    def __init__(self, steps):
        self.outputFile = ''
        self.steps = steps

    def set_monitoring_file(self, fileName):
        self.outputFile = fileName

    def as_list(self):
        return [self.as_tuple()]

    def as_tuple(self):
        return self._get_reader_collector_pair()

    def _get_reader_collector_pair(self):
        rc_pair = None
        at_selection = self._convert_to_alphatwirl()
        if self.outputFile:
            rc_pair = cut_flow_with_counter(
                at_selection, self.outputFile,
            )
        else:
            rc_pair = cut_flow(at_selection)
        return rc_pair[0]

    def _convert_to_alphatwirl(self, ati_dict=None):
        at_dict = {}
        if ati_dict is None:
            ati_dict = self.steps

        for k, cuts in ati_dict.items():
            if isinstance(cuts, dict):
                at_dict[k] = self._convert_to_alphatwirl(cuts)
            else:
                if isinstance(cuts, six.string_types):
                    cuts = [cuts]
                at_cuts = []
                for c in cuts:
                    if isinstance(c, dict):
                        at_cuts.append(self._convert_to_alphatwirl(c))
                    else:
                        at_cuts.append('ev: ev.{0}'.format(c))
                at_dict[k] = tuple(at_cuts)

        return at_dict
