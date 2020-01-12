from pygmalion.genmodel.insertion_statistics_formatter import InsertionStatisticsFormatter
from pygmalion.genmodel.nicknames import Nicknames
from utils import *


def test_1__test_tra(genmodelwrapper_1516_TRA):
    l = InsertionStatisticsFormatter._LENGTHS.get(Nicknames.vj_ins.value)
    stats = genmodelwrapper_1516_TRA.get_insertion_lengths(Nicknames.vj_ins.value)
    assert (len(stats) == l)

def test_2__test_trb(genmodelwrapper_1516_TRB):
    l = InsertionStatisticsFormatter._LENGTHS.get(Nicknames.vd_ins.value)
    stats = genmodelwrapper_1516_TRB.get_insertion_lengths(Nicknames.vd_ins.value)
    assert (len(stats) == l)
    l = InsertionStatisticsFormatter._LENGTHS.get(Nicknames.dj_ins.value)
    stats = genmodelwrapper_1516_TRB.get_insertion_lengths(Nicknames.dj_ins.value)
    assert (len(stats) == l)
