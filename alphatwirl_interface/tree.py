import alphatwirl as at
from alphatwirl_interface.completions import to_null_collector_pairs
from copy import deepcopy


class EventBuilder(object):

    def __init__(self, tree, max_events=-1):
        self.tree = tree
        self.max_events = max_events

    def __repr__(self):
        name_value_pairs = (
            ('tree', self.tree),
            ('max_events', self.max_events),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def __call__(self):
        events = at.roottree.BEvents(self.tree, maxEvents=self.max_events)
        return events


class Tree(object):

    def __init__(self, tree):
        self.tree = tree

    def __repr__(self):
        name_value_pairs = (
            ('tree', self.tree),
        )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(['{} = {!r}'.format(n, v) for n, v in name_value_pairs]),
        )

    def summarize(self, tblcfg, max_events=-1, modules=[]):
        reader_collector_pairs = modules

        reader_collector_pairs += [
            build_counter_collector_pair(c) for c in tblcfg]

        reader = at.loop.ReaderComposite()
        collector = at.loop.CollectorComposite()
        for r, c in reader_collector_pairs:
            reader.add(r)
            collector.add(c)

        eventBuilder = EventBuilder(self.tree, max_events=max_events)
        eventLoop = at.loop.EventLoop(eventBuilder, reader)
        reader = eventLoop()

        return collector.collect(((None, (reader, )), ))

    def scan(self, tblcfg, max_events=10, modules=[]):
        default_cfg = dict(
            keyAttrNames=(),
            sort=False,
            summaryClass=at.summary.Scan,
            outFile=False,
        )
        tblcfg = _complement_tblcfg_with_default(tblcfg, default_cfg)

        tableConfigCompleter = at.configure.TableConfigCompleter(
            defaultSummaryClass=at.summary.Count,
            createOutFileName=at.configure.TableFileNameComposer(
                default_prefix='tbl_n')
        )
        tblcfg = [tableConfigCompleter.complete(c) for c in tblcfg]

        return self.summarize(
            tblcfg,
            max_events=max_events,
            modules=modules,
        )


def _complement_tblcfg_with_default(tblcfg, default_cfg):
    for cfg in tblcfg:
        for k, v in default_cfg.items():
            cfg.setdefault(k, default=deepcopy(v))
    return tblcfg


def build_counter_collector_pair(tblcfg):
    keyValComposer = at.summary.KeyValueComposer(
        binnings=tblcfg['binnings'],
        keyIndices=tblcfg['keyIndices'],
        valAttrNames=tblcfg['valAttrNames'],
        valIndices=tblcfg['valIndices'],
    )

    nextKeyComposer = None
    if tblcfg['binnings'] is not None:
        nextKeyComposer = at.summary.NextKeyComposer(tblcfg['binnings'])

    summarizer = at.summary.Summarizer(
        Summary=tblcfg['summaryClass'],
    )
    reader = at.summary.Reader(
        keyValComposer=keyValComposer,
        summarizer=summarizer,
        nextKeyComposer=nextKeyComposer,
        weightCalculator=tblcfg['weight'],
        nevents=tblcfg['nevents'],
    )
    resultsCombinationMethod = at.collector.ToDataFrame(
        summaryColumnNames=tblcfg.outputColumns,
    )

    deliveryMethod = None
    collector = at.loop.Collector(
        resultsCombinationMethod, deliveryMethod)
    return reader, collector
