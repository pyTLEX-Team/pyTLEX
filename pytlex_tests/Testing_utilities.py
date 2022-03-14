import random
from typing import Optional

from pytlex_core import TCSP_solver
from pytlex_core.Event import Event
from pytlex_core.Instance import Instance
from pytlex_core.TimeX import TimeX
from pytlex_core.Signal import Signal
from pytlex_core.Link import Link
from pytlex_core import Graph

next_id = 0

failed_parse = ['ABC19980304.1830.1636.tml', 'APW19980213.1320.tml', 'APW19980227.0468.tml', 'APW19980227.0489.tml']

def consistent_graph_1() -> Graph:
    graph = Graph.Graph()

    node1 = TimeX(50, "FUTURE_REF", True, "next wednesday")
    node2 = TimeX(51, "FUTURE_REF", True, "next thursday")
    link1 = Link(50, "TLINK", "BEFORE", node1, node2)

    graph.nodes.add(node1)
    graph.nodes.add(node2)
    graph.links.add(link1)

    return graph


def consistent_graph_2() -> Graph:
    graph = Graph.Graph()

    node1 = TimeX(50, "FUTURE_REF", True, "next wednesday")
    node2 = TimeX(51, "FUTURE_REF", True, "next thursday")
    node3 = TimeX(52, "FUTURE_REF", True, "next friday")
    link1 = Link(50, "TLINK", "BEFORE", node1, node2)
    link2 = Link(51, "TLINK", "BEFORE", node2, node3)

    graph.nodes.add(node1)
    graph.nodes.add(node2)
    graph.nodes.add(node3)
    graph.links.add(link1)
    graph.links.add(link2)

    return graph


def consistent_graph_3() -> Graph:
    graph = Graph.Graph()

    event1 = Event(10, "REPORTING", "Test Stem1")
    event2 = Event(11, "PERCEPTION", "Test Stem2")

    node1 = TimeX(50, "FUTURE_REF", True, "next wednesday")
    node2 = TimeX(51, "FUTURE_REF", True, "next thursday")
    node3 = Instance(52, event1, "PAST", "PROGRESSIVE", "NOUN", "POS")
    node4 = Instance(53, event2, "PRESENT", "PERFECTIVE", "VERB", "POS")

    link1 = Link(54, "TLINK", "INCLUDES", node1, node3)
    link2 = Link(55, "ALINK", "INITIATES", node4, node2)
    link3 = Link(56, "TLINK", "AFTER", node2, node1)

    graph.nodes.add(node1)
    graph.nodes.add(node2)
    graph.nodes.add(node3)
    graph.nodes.add(node4)

    graph.links.add(link1)
    graph.links.add(link2)
    graph.links.add(link3)

    return graph


def consistent_graph_4() -> Graph:
    graph = Graph.Graph()

    node1 = TimeX(50, "FUTURE_REF", True, "next wednesday")
    node2 = TimeX(51, "FUTURE_REF", True, "next thursday")

    event1 = Event(10, "REPORTING", "Test Stem1")
    node3 = Instance(52, event1, "PAST", "PROGRESSIVE", "NOUN", "POS")

    link1 = Link(54, "TLINK", "BEFORE", node1, node2)
    link2 = Link(55, "SLINK", "MODAL", node2, node3)

    graph.nodes.add(node1)
    graph.nodes.add(node2)
    graph.nodes.add(node3)

    graph.links.add(link1)
    graph.links.add(link2)

    return graph


def consistent_graph_5() -> Graph:
    graph = Graph.Graph()

    node1 = TimeX(50, "FUTURE_REF", True, "next wednesday")
    node2 = TimeX(51, "FUTURE_REF", True, "next thursday")

    event1 = Event(10, "REPORTING", "Test Stem1")
    node3 = Instance(52, event1, "PAST", "PROGRESSIVE", "NOUN", "POS")
    node4 = TimeX(51, "FUTURE_REF", True, "some imaginary time")

    link1 = Link(54, "TLINK", "BEFORE", node1, node2)
    link2 = Link(55, "SLINK", "MODAL", node2, node3)
    link3 = Link(56, "TLINK", "AFTER", node3, node4)

    graph.nodes.add(node1)
    graph.nodes.add(node2)
    graph.nodes.add(node3)
    graph.nodes.add(node4)

    graph.links.add(link1)
    graph.links.add(link2)
    graph.links.add(link3)

    return graph


def consistent_graph_6() -> Graph:
    t50 = test_timex(50)
    t51 = test_timex()
    t52 = test_timex()
    t53 = test_timex()
    t54 = test_timex()
    t55 = test_timex()
    t56 = test_timex()

    link1 = Link(1, "TLINK", "BEFORE", t50, t51)
    link2 = Link(2, "TLINK", "BEFORE", t51, t52)
    link3 = Link(3, "SLINK", "MODAL", t51, t53)
    link4 = Link(4, "TLINK", "INCLUDES", t53, t54)
    link5 = Link(5, "SLINK", "MODAL", t51, t55)
    link6 = Link(6, "TLINK", "INCLUDES", t55, t56)

    nodes = {t50, t51, t52, t53, t54, t55, t56}
    links = {link1, link2, link3, link4, link5, link6}

    return Graph.Graph(nodes=nodes, links=links)


def consistent_graph_7() -> Graph:
    t1 = test_timex(1)
    t2 = test_timex()
    t3 = test_timex()
    t4 = test_timex()
    t5 = test_timex()
    t6 = test_timex()
    t7 = test_timex()
    t8 = test_timex()
    t9 = test_timex()
    t10 = test_timex()
    t11 = test_timex()
    t12 = test_timex()
    t13 = test_timex()
    t14 = test_timex()
    t15 = test_timex()

    link1 = Link(1, "TLINK", "BEFORE", t1, t2)
    link2 = Link(2, "TLINK", "BEFORE", t2, t13)
    link3 = Link(3, "SLINK", "FACTIVE", t2, t13)
    link4 = Link(4, "TLINK", "BEFORE", t2, t3)
    link5 = Link(5, "SLINK", "COUNTER_FACTIVE", t2, t5)
    link6 = Link(6, "TLINK", "BEFORE", t5, t6)
    link7 = Link(7, "TLINK", "IDENTITY", t3, t4)
    link8 = Link(8, "SLINK", "MODAL", t3, t7)
    link9 = Link(9, "SLINK", "MODAL", t4, t8)
    link10 = Link(10, "TLINK", "IDENTITY", t7, t8)
    link11 = Link(11, "TLINK", "INCLUDES", t13, t14)
    link12 = Link(12, "TLINK", "ENDED_BY", t14, t15)
    link13 = Link(13, "TLINK", "DURING", t8, t9)
    link14 = Link(14, "TLINK", "DURING", t9, t10)
    link15 = Link(15, "TLINK", "DURING", t10, t11)
    link16 = Link(16, "SLINK", "EVIDENTIAL", t11, t12)
    link17 = Link(17, "TLINK", "IBEFORE", t11, t12)

    nodes = {t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15}

    links = {link1, link2, link3, link4, link5, link6
        , link7, link8, link9, link10, link11, link12
        , link13, link14, link15, link16, link17}

    return Graph.Graph(nodes=nodes, links=links)


def consistent_graph_8() -> Graph:
    t1 = test_timex(1)
    t2 = test_timex()
    t3 = test_timex()
    t4 = test_timex()
    t5 = test_timex()
    t6 = test_timex()
    t7 = test_timex()
    t8 = test_timex()
    t9 = test_timex()
    t10 = test_timex()
    t11 = test_timex()
    t12 = test_timex()
    t13 = test_timex()

    link1 = Link(1, "TLINK", "IBEFORE", t1, t2)
    link2 = Link(2, "TLINK", "ENDS", t2, t3)
    link3 = Link(3, "TLINK", "BEGINS", t1, t3)
    link4 = Link(4, "TLINK", "BEGINS", t2, t4)
    link5 = Link(5, "TLINK", "ENDS", t5, t4)
    link6 = Link(6, "TLINK", "ENDS", t5, t6)
    link7 = Link(7, "TLINK", "BEGINS", t3, t6)
    link8 = Link(8, "TLINK", "AFTER", t7, t6)
    link9 = Link(9, "TLINK", "AFTER", t8, t7)
    link10 = Link(10, "TLINK", "BEGUN_BY", t9, t7)
    link11 = Link(11, "TLINK", "ENDED_BY", t9, t8)
    link12 = Link(12, "TLINK", "ENDS", t9, t10)
    link13 = Link(13, "TLINK", "IAFTER", t10, t6)
    link14 = Link(14, "TLINK", "BEGUN_BY", t11, t5)
    link15 = Link(15, "TLINK", "ENDS", t10, t11)
    link16 = Link(16, "TLINK", "INCLUDES", t12, t11)
    link17 = Link(17, "TLINK", "BEGINS", t13, t12)
    link18 = Link(18, "TLINK", "IBEFORE", t13, t5)
    link19 = Link(19, "TLINK", "INCLUDES", t4, t13)

    nodes_set = {t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13}
    link_set = {link1, link2, link3, link4, link5, link6, link7, link8, link9, link10, link11, link12, link13,
                link14, link15, link16, link17, link18, link19}
    return Graph.Graph(nodes=nodes_set, links=link_set)


def consistent_graph_9() -> Graph:
    t1 = test_timex(1)
    t2 = test_timex()
    t3 = test_timex()
    t4 = test_timex()
    t5 = test_timex()
    t6 = test_timex()
    t7 = test_timex()
    t8 = test_timex()
    t9 = test_timex()

    link1 = Link(1, "TLINK", "BEGUN_BY", t1, t2)
    link2 = Link(2, "TLINK", "IAFTER", t3, t2)
    link3 = Link(3, "TLINK", "IAFTER", t4, t3)
    link4 = Link(4, "TLINK", "ENDS", t4, t1)
    link5 = Link(5, "TLINK", "ENDS", t4, t5)
    link6 = Link(6, "TLINK", "BEGUN_BY", t5, t3)
    link7 = Link(7, "TLINK", "INCLUDES", t2, t6)
    link8 = Link(8, "TLINK", "ENDS", t7, t2)
    link9 = Link(9, "TLINK", "IBEFORE", t6, t7)
    link10 = Link(10, "TLINK", "IBEFORE", t7, t8)
    link11 = Link(11, "TLINK", "IAFTER", t9, t8)
    link12 = Link(12, "TLINK", "ENDS", t9, t1)

    node_set = {t1, t2, t3, t4, t5, t6, t7, t8, t9}
    link_set = {link1, link2, link3, link4, link5, link6, link7, link8, link9, link10, link11, link12}

    return Graph.Graph(nodes=node_set, links=link_set)


def consistent_graph_10() -> Graph:
    t1 = test_timex(1)
    t2 = test_timex()
    t3 = test_timex()
    t4 = test_timex()
    t5 = test_timex()
    t6 = test_timex()
    t7 = test_timex()
    t8 = test_timex()

    link1 = Link(1, "TLINK", "IBEFORE", t1, t2)
    link2 = Link(2, "TLINK", "ENDS", t2, t3)
    link3 = Link(3, "TLINK", "BEGINS", t1, t3)
    link4 = Link(4, "TLINK", "IAFTER", t4, t3)
    link5 = Link(5, "TLINK", "ENDS", t4, t5)
    link6 = Link(6, "TLINK", "BEGINS", t3, t5)
    link7 = Link(7, "TLINK", "IDENTITY", t4, t6)
    link8 = Link(8, "TLINK", "AFTER", t7, t6)
    link9 = Link(9, "TLINK", "ENDS", t7, t8)
    link10 = Link(10, "TLINK", "IAFTER", t8, t6)

    node_set = {t1, t2, t3, t4, t5, t6, t7, t8}
    link_set = {link1, link2, link3, link4, link5, link6, link7, link8, link9, link10}

    return Graph.Graph(nodes=node_set, links=link_set)


def consistent_graph_11() -> Graph:
    t1 = test_timex(1)
    t2 = test_timex()
    t3 = test_timex()
    t4 = test_timex()
    t5 = test_timex()
    t6 = test_timex()
    t7 = test_timex()
    t8 = test_timex()
    t9 = test_timex()
    t10 = test_timex()
    t11 = test_timex()
    t12 = test_timex()
    t13 = test_timex()
    t14 = test_timex()
    t15 = test_timex()
    t16 = test_timex()
    t17 = test_timex()
    t18 = test_timex()
    t19 = test_timex()
    t20 = test_timex()
    t21 = test_timex()
    t22 = test_timex()
    t23 = test_timex()
    t24 = test_timex()
    t25 = test_timex()
    t26 = test_timex()

    l1 = Link(1, "TLINK", "BEFORE", t1, t2)
    l2 = Link(2, "TLINK", "BEFORE", t3, t2)
    l3 = Link(3, "TLINK", "AFTER", t4, t5)
    l4 = Link(4, "TLINK", "SIMULTANEOUS", t6, t7)
    l5 = Link(5, "TLINK", "IS_INCLUDED", t8, t9)
    l6 = Link(6, "TLINK", "DURING", t10, t2)
    l7 = Link(7, "ALINK", "INITIATES", t11, t10)
    l8 = Link(8, "TLINK", "BEFORE", t12, t2)
    l9 = Link(9, "TLINK", "BEFORE", t8, t2)
    l10 = Link(10, "TLINK", "IS_INCLUDED", t13, t9)
    l11 = Link(11, "TLINK", "AFTER", t14, t2)
    l12 = Link(12, "TLINK", "INCLUDES", t9, t3)
    l13 = Link(13, "TLINK", "AFTER", t18, t5)
    l14 = Link(14, "TLINK", "AFTER", t11, t15)
    l15 = Link(15, "TLINK", "BEFORE", t16, t2)
    l16 = Link(16, "TLINK", "BEFORE", t17, t19)
    l17 = Link(17, "TLINK", "AFTER", t7, t14)
    l18 = Link(18, "TLINK", "BEFORE", t20, t2)
    l19 = Link(19, "TLINK", "AFTER", t21, t2)
    l20 = Link(20, "TLINK", "AFTER", t19, t18)
    l21 = Link(21, "TLINK", "IDENTITY", t22, t23)
    l22 = Link(22, "TLINK", "AFTER", t22, t14)
    l23 = Link(23, "TLINK", "BEFORE", t13, t2)
    l24 = Link(24, "TLINK", "INCLUDES", t19, t16)
    l25 = Link(25, "TLINK", "AFTER", t11, t24)
    l26 = Link(26, "TLINK", "IDENTITY", t5, t1)
    l27 = Link(27, "TLINK", "BEFORE", t26, t18)
    l28 = Link(28, "TLINK", "INCLUDES", t9, t2)
    l29 = Link(29, "TLINK", "BEFORE", t17, t18)
    l30 = Link(30, "TLINK", "INCLUDES", t18, t14)
    l31 = Link(31, "TLINK", "AFTER", t25, t14)
    l32 = Link(32, "TLINK", "INCLUDES", t17, t2)

    return Graph.Graph({t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26},
                 {l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20, l21, l22, l23, l24, l25, l26, l27, l28, l29, l30, l31, l32})


def wsj_0006() -> Graph:
    event1 = Event(1, "REPORTING", "test_stem")
    event2 = Event(2, "OCCURRENCE", "test_stem")
    event8 = Event(8, "OCCURRENCE", "test_stem")
    event4 = Event(4, "REPORTING", "test_stem")
    event5 = Event(5, "I_STATE", "test_stem")
    event6 = Event(6, "OCCURRENCE", "test_stem")
    event19 = Event(19, "OCCURRENCE", "test_stem")
    event7 = Event(7, "ASPECTUAL", "test_stem")
    event20 = Event(20, "OCCURRENCE", "test_stem")

    node79 = Instance(79, event19, "NONE", "NONE", "NOUN", "POS")
    node76 = Instance(76, event4, "PAST", "NONE", "VERB", "POS")
    node77 = Instance(77, event5, "PRESENT", "NONE", "VERB", "POS")
    node73 = Instance(73, event1, "PAST", "NONE", "VERB", "POS")
    node81 = Instance(81, event20, "NONE", "NONE", "NOUN", "POS")
    node74 = Instance(74, event2, "PAST", "NONE", "VERB", "POS")
    node80 = Instance(80, event7, "PRESENT", "NONE", "VERB", "POS")
    node78 = Instance(78, event6, "INFINITIVE", "NONE", "VERB", "POS")
    node75 = Instance(75, event8, "NONE", "NONE", "NOUN", "POS")

    node10 = TimeX(9, "1989-11-02", False, "11/02/89", "DATE", "NONE", "CREATION_TIME")
    node11 = TimeX(10, "1989-12-31", True, "year-end", "DATE", "NONE", "NONE", 9)

    signal1 = Signal(12, "by")

    link1 = Link(1, "TLINK", "BEFORE", node80, node11, signal1)
    link2 = Link(2, "TLINK", "BEFORE", node73, node10)
    link3 = Link(3, "TLINK", "BEFORE", node74, node73)
    link4 = Link(4, "TLINK", "AFTER", node74, node75)
    link5 = Link(5, "TLINK", "SIMULTANEOUS", node76, node73)
    link6 = Link(6, "TLINK", "ENDS", node80, node81)

    link13 = Link(13, "SLINK", "MODAL", node74, node75)
    link7 = Link(7, "SLINK", "EVIDENTIAL", node73, node74)
    link8 = Link(8, "SLINK", "EVIDENTIAL", node76, node77)
    link9 = Link(9, "SLINK", "MODAL", node77, node78)
    link10 = Link(10, "SLINK", "FACTIVE", node78, node79)
    link11 = Link(11, "SLINK", "MODAL", node77, node80)

    link12 = Link(12, "ALINK", "CULMINATES", node80, node81)

    nodes = {node79, node76, node77, node73, node81, node74, node80, node78, node75, node10, node11}
    links = {link1, link2, link3, link4, link5, link6, link7, link8, link9, link10, link11, link12, link13}

    return Graph.Graph(nodes=nodes, links=links)


def wsj_1073() -> Graph:
    event2 = Event(2, "REPORTING", "say")
    event3 = Event(3, "OCCURRENCE", "purchase")
    event4 = Event(4, "OCCURRENCE", "pay")
    event9 = Event(9, "OCCURRENCE", "have")
    event30 = Event(30, "OCCURRENCE", "sale")

    node1989 = Instance(1989, event2, "PAST", "NONE", "VERB", "POS")
    node1990 = Instance(1990, event3, "PAST", "NONE", "VERB", "POS")
    node1991 = Instance(1991, event4, "PAST", "NONE", "VERB", "POS")
    node1992 = Instance(1992, event9, "PAST", "PERFECTIVE", "VERB", "POS")
    node1993 = Instance(1993, event30, "NONE", "NONE", "NOUN", "POS")

    node11 = TimeX(11, "1989-10-25", False, "10/25/89", "DATE", "NONE", "CREATION_TIME")
    node31 = TimeX(31, "1988", True, "last year", "DATE", "NONE", "NONE", 11)

    link1 = Link(1, "TLINK", "SIMULTANEOUS", node1992, node1993, None, "USER")
    link2 = Link(2, "TLINK", "BEFORE", node1991, node11, None, "USER")
    link3 = Link(3, "TLINK", "BEFORE", node1989, node11, None, "USER")
    link4 = Link(4, "TLINK", "BEFORE", node1992, node11, None, "USER")
    link5 = Link(5, "TLINK", "BEFORE", node1993, node31, None, "USER")

    link6 = Link(6, "SLINK", "EVIDENTIAL", node1989, node1990)

    nodes = {node1989, node1990, node1991, node1992, node1993, node11, node31}
    links = {link1, link2, link3, link4, link5, link6}

    return Graph.Graph(nodes=nodes, links=links)


def wsj_0555() -> Graph:
    event1 = Event(1, "REPORTING", "test_stem")
    event11 = Event(11, "STATE", "test_stem")
    event2 = Event(2, "I_ACTION", "test_stem")
    event4 = Event(4, "OCCURRENCE", "test_stem")
    event6 = Event(6, "REPORTING", "test_stem")
    event7 = Event(7, "STATE", "test_stem")

    node44 = Instance(44, event1, "PAST", "NONE", "VERB", "POS")
    node49 = Instance(49, event7, "PRESENT", "NONE", "VERB", "POS")
    node46 = Instance(46, event2, "PRESENT", "PERFECTIVE", "VERB", "POS")
    node47 = Instance(47, event4, "INFINITIVE", "NONE", "VERB", "POS")
    node45 = Instance(45, event11, "NONE", "NONE", "ADJECTIVE", "POS")
    node48 = Instance(48, event6, "PAST", "NONE", "VERB", "POS")

    node12 = TimeX(12, "1989-10-30", False, "10/30/89", "DATE", "NONE", "CREATION_TIME")
    node13 = TimeX(13, "2007-03-15", False, "March 15, 2007", "DATE", "NONE", "NONE")

    link1 = Link(1, "TLINK", "BEFORE", node44, node12)
    link2 = Link(2, "TLINK", "ENDED_BY", node45, node13)
    link3 = Link(3, "TLINK", "BEFORE", node46, node44)
    link4 = Link(4, "TLINK", "IDENTITY", node48, node44)

    link5 = Link(5, "SLINK", "EVIDENTIAL", node44, node46)
    link6 = Link(6, "SLINK", "MODAL", node46, node47)
    link7 = Link(7, "SLINK", "EVIDENTIAL", node48, node49)

    nodes = {node44, node49, node46, node47, node45, node48, node12, node13}
    links = {link1, link2, link3, link4, link5, link6, link7}

    return Graph.Graph(nodes=nodes, links=links)


def wsj_0032_inconsistent() -> Graph:
    ei103 = test_instance(103)
    ei112 = test_instance(112)
    ei104 = test_instance(104)
    ei111 = test_instance(111)
    ei106 = test_instance(106)
    ei107 = test_instance(107)
    ei110 = test_instance(110)
    ei105 = test_instance(105)
    ei109 = test_instance(109)
    ei102 = test_instance(102)
    ei108 = test_instance(108)

    t13 = test_timex(13)
    t19 = test_timex(19)
    t18 = test_timex(18)
    t17 = test_timex(17)
    t21 = test_timex(21)

    nodes = {ei103, ei112, ei104, ei111, ei106, ei107, ei110, ei105,
             ei109, ei102, ei108, t13, t17, t18, t19, t21}

    link25 = Link(25, "TLINK", "IS_INCLUDED", ei106, t13)
    link1 = Link(1, "TLINK", "IS_INCLUDED", ei110, t13)
    link2 = Link(2, "TLINK", "AFTER", t13, ei102)
    link3 = Link(3, "TLINK", "BEGINS", ei102, ei103)
    link4 = Link(4, "TLINK", "IDENTITY", ei104, ei103)
    link5 = Link(5, "TLINK", "BEFORE", ei104, ei105)
    link6 = Link(6, "TLINK", "IS_INCLUDED", ei105, t19)
    link7 = Link(7, "TLINK", "IDENTITY", t19, t13)
    link8 = Link(8, "TLINK", "BEFORE", ei104, ei107)
    link9 = Link(9, "TLINK", "ENDED_BY", ei107, t18)
    link10 = Link(10, "TLINK", "INCLUDES", t17, t13)
    link11 = Link(11, "TLINK", "INCLUDES", t17, ei108)
    link12 = Link(12, "TLINK", "IDENTITY", ei109, ei104)
    link13 = Link(13, "TLINK", "BEGUN_BY", ei109, ei110)
    link14 = Link(14, "TLINK", "AFTER", ei110, ei112)
    link15 = Link(15, "TLINK", "BEFORE", ei112, ei111)
    link16 = Link(16, "TLINK", "SIMULTANEOUS", ei111, t21)
    link17 = Link(17, "TLINK", "BEFORE", t21, t13)

    link18 = Link(18, "SLINK", "EVIDENTIAL", ei111, ei112)
    link21 = Link(21, "SLINK", "FACTIVE", ei110, ei112)
    link22 = Link(22, "SLINK", "EVIDENTIAL", ei105, ei104)
    link23 = Link(23, "SLINK", "MODAL", ei106, ei107)

    link19 = Link(19, "ALINK", "INITIATES", ei102, ei103)

    links = {link1, link2, link3, link4, link5, link6, link7, link8, link9, link10, link11, link12,
             link13, link14, link15, link16, link17, link18, link19, link21, link22, link23, link25}

    return Graph.Graph(nodes=nodes, links=links)


def inconsistent_graph_1_self_loop() -> Graph:
    graph = Graph.Graph()

    node1 = TimeX(50, "FUTURE_REF", True, "next wednesday")
    node2 = TimeX(51, "FUTURE_REF", True, "next thursday")

    graph.nodes.add(node1)
    graph.nodes.add(node2)

    link1 = Link(52, "SLINK", "MODAL", node1, node2)
    link2 = Link(53, "TLINK", "INCLUDES", node2, node2)

    graph.links.add(link1)
    graph.links.add(link2)

    return graph


def inconsistent_graph_2_self_loop() -> Graph:
    graph = Graph.Graph()

    node1 = TimeX(50, "FUTURE_REF", True, "next wednesday")
    graph.nodes.add(node1)
    graph.links.add(Link(51, "TLINK", "BEFORE", node1, node1))

    return graph


def inconsistent_graph_3() -> Graph:
    graph = Graph.Graph()

    node1 = test_timex()
    node2 = test_timex()
    node3 = test_timex()

    link1 = Link(1, "TLINK", "BEFORE", node1, node2)
    link2 = Link(2, "TLINK", "BEFORE", node2, node3)
    link3 = Link(3, "TLINK", "BEFORE", node3, node1)

    node_set = {node1, node2, node3}
    link_set = {link1, link2, link3}

    return Graph.Graph(nodes=node_set, links=link_set)


def inconsistent_graph_4() -> Graph:
    graph = Graph.Graph()

    node1 = test_timex()
    node2 = test_timex()
    node3 = test_timex()
    node4 = test_timex(49)

    link1 = Link(1, "TLINK", "BEFORE", node1, node2)
    link2 = Link(2, "TLINK", "BEFORE", node2, node3)
    link3 = Link(3, "TLINK", "BEFORE", node3, node1)
    link4 = Link(4, "SLINK", "MODAL", node4, node1)

    node_set = {node1, node2, node3, node4}
    link_set = {link1, link2, link3, link4}

    return Graph.Graph(nodes=node_set, links=link_set)


def inconsistent_graph_5() -> Graph:

    node1 = test_timex()
    node2 = test_timex()
    node3 = test_timex()
    node4 = test_timex()
    node5 = test_timex()
    node6 = test_timex()
    node7 = test_timex()

    link1 = Link(1, "TLINK", "INCLUDES", node1, node2)
    link2 = Link(2, "TLINK", "BEFORE", node2, node3)
    link3 = Link(3, "TLINK", "BEFORE", node3, node4)
    link4 = Link(4, "TLINK", "BEFORE", node4, node2)
    link5 = Link(5, "TLINK", "ENDS", node3, node5)
    link6 = Link(6, "TLINK", "AFTER", node5, node6)
    link7 = Link(7, "TLINK", "BEGINS", node6, node7)
    link7 = Link(7, "TLINK", "AFTER", node6, node7)

    node_set = {node1, node2, node3, node4, node5, node6, node7}
    link_set = {link1, link2, link3, link4, link5, link6, link7}

    return Graph.Graph(nodes=node_set, links=link_set)


def inconsistent_graph_6() -> Graph:
    node1 = test_timex()
    node2 = test_timex()

    link1 = Link(1, "TLINK", "INCLUDES", node1, node2)
    link2 = Link(2, "TLINK", "ENDED_BY", node1, node2)

    node_set = {node1, node2}
    link_set = {link1, link2}

    return Graph.Graph(nodes=node_set, links=link_set)


def inconsistent_graph_7() -> Graph:
    node1 = test_timex()
    node2 = test_timex()
    node3 = test_timex()

    link1 = Link(1, "TLINK", "BEFORE", node1, node2)
    link2 = Link(2, "TLINK", "IAFTER", node2, node3)
    link3 = Link(3, "TLINK", "ENDED_BY", node1, node3)

    node_set = {node1, node2, node3}
    link_set = {link1, link2, link3}

    return Graph.Graph(nodes=node_set, links=link_set)


def indeterminant_graph_1() -> Graph:
    node1 = test_timex()
    node2 = test_timex()
    node3 = test_timex()
    node4 = test_timex()
    node5 = test_timex()

    link1 = Link(1, "TLINK", "BEFORE", node1, node2)
    link2 = Link(2, "TLINK", "BEFORE", node1, node3)
    link3 = Link(3, "TLINK", "BEFORE", node2, node4)
    link4 = Link(4, "TLINK", "BEFORE", node3, node4)
    link5 = Link(5, "TLINK", "BEFORE", node4, node5)

    node_set = {node1, node2, node3, node4, node5}
    link_set = {link1, link2, link3, link4, link5}

    return Graph.Graph(nodes=node_set, links=link_set)


def test_timex(tid: Optional[int] = None):
    global next_id
    if tid is None:
        next_id += 1
    else:
        next_id = tid
    return TimeX(next_id, "Test Value", True, "Test Phrase")


def test_signal(sid: Optional[int] = None):
    global next_id
    if sid is None:
        next_id += 1
    else:
        next_id = sid
    return Signal(next_id, "Test Signal")


def test_event(eid: Optional[int] = None):
    global next_id
    if eid is None:
        next_id += 1
    else:
        next_id = eid
    return Event(next_id, "REPORTING", "Test Stem")


def test_instance(eiid: Optional[int] = None):
    global next_id
    if eiid is None:
        next_id += 1
    else:
        next_id = eiid
    return Instance(next_id, test_event(), "PAST", "NONE", "NOUN", "POS")


def _inconsistent_functions() -> list[str]:
    graph_functions = []

    graph_functions.append('inconsistent_graph_1_self_loop')
    graph_functions.append('inconsistent_graph_2_self_loop')
    graph_functions.append('inconsistent_graph_3')
    graph_functions.append('inconsistent_graph_4')
    graph_functions.append('inconsistent_graph_5')
    graph_functions.append('inconsistent_graph_6')
    graph_functions.append('inconsistent_graph_7')

    return  graph_functions


def _consistent_functions() -> list[str]:
    graph_functions = []

    graph_functions.append('consistent_graph_1')
    graph_functions.append('consistent_graph_2')
    graph_functions.append('consistent_graph_3')
    graph_functions.append('consistent_graph_4')
    graph_functions.append('consistent_graph_5')
    graph_functions.append('consistent_graph_6')
    graph_functions.append('consistent_graph_7')
    graph_functions.append('consistent_graph_8')
    graph_functions.append('consistent_graph_9')
    graph_functions.append('consistent_graph_10')

    return graph_functions


def random_graph(consistent: Optional[bool] = None) -> Graph:
    if consistent is not None:
        if consistent:
            return globals()[random.choice(_consistent_functions())]()
        elif not consistent:
            return globals()[random.choice(_inconsistent_functions())]
    else:
        return globals()[random.choice(_consistent_functions() + _inconsistent_functions())]


def all_graphs(consistent: Optional[bool] = None) -> list[Graph]:
    if consistent is not None:
        if consistent:
            return [globals()[function]() for function in _consistent_functions()]
        else:
            return [globals()[function]() for function in _inconsistent_functions()]
    else:
        return [globals()[function]() for function in _consistent_functions() + _inconsistent_functions()]


if __name__ == '__main__':
    print(len(_consistent_functions()))
    print(len(_inconsistent_functions()))
    print(len(_consistent_functions() + _inconsistent_functions()))
