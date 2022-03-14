import os
from pytlex_core import Sanity_Check
from pytlex_tests import Testing_utilities


def try_sco_identity_rule():
    filepath = r"../pytlex_data/TimeBankCorpus/wsj_0586.tml"
    Sanity_Check.sco_identity_rule(filepath)

def try_orphaned_node_rule():
    filepath = r"../pytlex_data/TimeBankCorpus/ABC19980108.1830.0711.tml"
    Sanity_Check.orphaned_node_rule(filepath)

def try_node_to_node_rule():
    filepath = r"../pytlex_data/TimeBankCorpus/PRI19980213.2000.0313.tml"
    Sanity_Check.node_to_node(filepath)

def try_perception_rule():
    filepath = r"../pytlex_data/TimeBankCorpus/ABC19980114.1830.0611.tml"
    Sanity_Check.perception_rule(filepath)

def try_repeating_links_rule():
    filepath = filepath = r"../pytlex_data/TimeBankCorpus/WSJ900813-0157.tml"
    Sanity_Check.repeating_links(filepath)

def try_conditional_slink_rule():
    filepath = r"../pytlex_data/TimeBankCorpus/WSJ900813-0157.tml"
    Sanity_Check.conditional_slink_rule(filepath)

def try_ALINK_rule():
    filepath = r"../pytlex_data/TimeBankCorpus/WSJ900813-0157.tml"
    Sanity_Check.ALINK_rule(filepath)

if __name__ == '__main__':
    try_sco_identity_rule()
    try_node_to_node_rule()
    try_perception_rule()
    try_repeating_links_rule()
    try_orphaned_node_rule()
    try_conditional_slink_rule()
    try_ALINK_rule()