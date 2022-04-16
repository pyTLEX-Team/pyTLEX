# Written by: vfern124
# Last updated: vfern124

from dataclasses import dataclass, field
from pytlex_core.Signal import Signal
from typing import Any


# Do not change order of variables, will cause TimeMLParser to explode... Alert vfern124 before making changes
@dataclass
class Link:
    """
    Link class represents an edge between a starting node and a related node.
    """
    link_id: int
    link_tag: str
    rel_type: str
    start_node: Any  # Must be Instance or TimeX
    related_to_node: Any  # Must be Instance or TimeX
    signal: Signal = field(default=None)
    origin_type: str = field(default=None)
    syntax: str = field(default=None)

    def __post_init__(self):
        if self.link_id < 0:
            raise Exception("Error: Link ID cannot be less than 0")

        accepted_origin_types = {"USER", "MANUALLY", "CLOSURE", None}
        if self.link_tag == 'TLINK' and self.origin_type not in accepted_origin_types:
            raise Exception("Error: Not acceptable Origin Type - " + self.origin_type)

        accepted_link_tags = {"ALINK", "SLINK", "TLINK"}
        if self.link_tag not in accepted_link_tags:
            raise Exception("Error: Not acceptable Link Tag - l" + str(self.link_id))

        accepted_alink_types = {"INITIATES", "CULMINATES", "TERMINATES", "CONTINUES", "REINITIATES"}
        if self.link_tag == 'ALINK' and self.rel_type not in accepted_alink_types:
            raise Exception("Error: Not acceptable Alink Relation Type - l" + str(self.link_id))

        accepted_slink_types = {"MODAL", "EVIDENTIAL", "NEG_EVIDENTIAL", "FACTIVE", "COUNTER_FACTIVE", "CONDITIONAL"}
        if self.link_tag == 'SLINK' and self.rel_type not in accepted_slink_types:
            raise Exception("Error: Not acceptable Slink Relation Type - l" + str(self.link_id))

        accepted_tlink_types = {"BEFORE", "AFTER", "INCLUDES", "IS_INCLUDED", "DURING", "DURING_INV", "SIMULTANEOUS",
                                "IAFTER", "IBEFORE", "IDENTITY", "BEGINS", "ENDS", "BEGUN_BY", "ENDED_BY"}
        if self.link_tag == 'TLINK' and self.rel_type not in accepted_tlink_types:
            raise Exception("Error: Not acceptable Tlink Relation Type - l" + str(self.link_id))

        if self.start_node is None:
            raise Exception("Error: Start Node cannot be None - l" + str(self.link_id))

        if self.related_to_node is None:
            raise Exception("Error: Related to Node cannot be None - l" + str(self.link_id))

        valid_types = {"<class 'Instance'>", "<class 'Instance.Instance'>", "<class 'pytlex_core.Instance.Instance'>",
                       "<class 'TimeX'>", "<class 'TimeX.TimeX'>", "<class 'pytlex_core.TimeX.TimeX'>"}
        if str(type(self.start_node)) not in valid_types:
            raise Exception("Error: Start Node must be Instance or TimeX - " + str(type(self.start_node)) + " - l" +
                            str(self.link_id))

        if str(type(self.related_to_node)) not in valid_types:
            raise Exception("Error: Related to Node must be Instance or TimeX - " + str(type(self.related_to_node)) +
                            " - l" + str(self.link_id))

    def get_id_str(self):
        return 'l' + str(self.link_id)

    def __hash__(self):
        return hash(str(self.link_id) + self.link_tag)

    def to_json(self):
        signal = self.signal.to_json() if self.signal is not None else "\"NULL\""
        origin_type = self.origin_type if self.origin_type is not None else "NULL"
        syntax = self.syntax if self.syntax is not None else "NULL"

        return f'{{"id":"{self.get_id_str()}", "tag":"{self.link_tag}", "rel_type":"{self.rel_type}", "eventInstance":"' \
               f'{self.start_node.get_id_str()}", "relatedToNode":"{self.related_to_node.get_id_str()}", ' \
               f'"signal":{signal}, "origin_type":"{origin_type}", "syntax":"{syntax}"}}'
