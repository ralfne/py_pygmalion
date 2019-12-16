from pygmalion.bayesian_network_importer.conditional_matrix import ConditionalMatrix

#
# class EventsMarginalsParser(object):
#     def __init__(self, pomgranate_bayesian_network):
#         self._items = {}
#         self._get_marginals_for_events(pomgranate_bayesian_network)
#
#     def _get_marginals_for_events(self, pomgranate_bayesian_network):
#         all_marginals = pomgranate_bayesian_network.marginal()
#         for m in all_marginals:
#             nickname = self._get_nickname_for_event_marginals(m)
#             self._items[nickname] = m.parameters[0]
#
#     def _get_nickname_for_event_marginals(self, event_marginals):
#         for key, value in event_marginals.parameters[0].iteritems():
#             i = key.find(ConditionalMatrix.EVENT_NICKNAME_REALIZATION_SEP)
#             out = key[0:i]
#             return out
#
#     def get_as_list(self, nickname):
#         out = []
#         item = self._items.get(nickname)
#         for key, value in item.iteritems():
#             row = []
#             row.append(key)
#             row.append(value)
#             out.append(row)
#         return out