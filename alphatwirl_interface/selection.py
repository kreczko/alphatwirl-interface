from collections import Sequence
from alphatwirl_interface.cut_flows import cut_flow, cut_flow_with_counter
import six


class Selection(object):

    def __init__(self, steps={}, monitoringFile=None):
        self.monitoringFile = monitoringFile
        self.steps = steps

    def set_monitoring_file(self, monitoringFile):
        self.monitoringFile = monitoringFile

    def as_list(self):
        return [self.as_tuple()]

    def as_tuple(self):
        return self._get_reader_collector_pair()

    def _get_reader_collector_pair(self):
        rc_pair = None
        if self.monitoringFile:
            rc_pair = cut_flow_with_counter(
                self.steps, self.monitoringFile,
            )
        else:
            rc_pair = cut_flow(self.steps)
        return rc_pair[0]
