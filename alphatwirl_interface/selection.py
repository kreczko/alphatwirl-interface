from collections import Sequence
from alphatwirl_interface.cut_flows import cut_flow, cut_flow_with_counter
import six


class Selection(object):
    '''
        This class ties together several modules from alphatwirl to
        bring a simplified Selection experience.

        :param dict steps: A dictionary of selection steps
        :param str cutflow_file: path to the cutflow output file.

        example:

          preselection = Selection(
              dict(
                All=(
                    'NMuon[0] == 2',
                    'muon_pt[0] > 20',
                    'muon_pt[1] > 20',
                    'Muon_Iso[0] < 0.1',
                    'Muon_Iso[1] < 0.1',
                    'Muon_Charge[0] == -1 * Muon_Charge[1]',
                )),
               'output/cutflow_preselection.txt'
          )

          # define in alphatwirl modules to pass to tree.scan
          modules = [
            preselection.as_tuple(),
            ...
          ]
    '''

    def __init__(self, steps={}, cutflow_file=None):
        self.cutflow_file = cutflow_file
        self.steps = steps

    def set_cutflow_file(self, cutflow_file):
        self.cutflow_file = cutflow_file

    def as_list(self):
        return [self.as_tuple()]

    def as_tuple(self):
        return self._get_reader_collector_pair()

    def _get_reader_collector_pair(self):
        rc_pair = None
        if self.cutflow_file:
            rc_pair = cut_flow_with_counter(
                self.steps, self.cutflow_file,
            )
        else:
            rc_pair = cut_flow(self.steps)
        return rc_pair[0]
