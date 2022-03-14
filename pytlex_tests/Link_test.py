# Written by: jsegr004
# Last updated: gparr014 - added tests for methods

import unittest
from pytlex_core.TimeX import TimeX
from pytlex_core.Link import Link
from pytlex_core.Instance import Instance
from pytlex_core.Event import Event
from pytlex_core.Signal import Signal

# Valid test inputs
timex0 = TimeX(1, 'value0', True, 'phrase0')
timex1 = TimeX(2, 'value1', True, 'phrase1')

event0 = Event(1, "I_STATE", "STEM")
event1 = Event(2, "I_STATE", "STEM")

instance0 = Instance(1, event0, "PAST", "PERFECTIVE", "ADJECTIVE", "POS")
instance1 = Instance(2, event1, "PRESENT", "PROGRESSIVE", "VERB", "NEG")

signal = Signal(1, 'signal')


class LinkTestCases(unittest.TestCase):
    def test_default(self):
        link0 = Link(0, 'ALINK', 'INITIATES', timex0, timex1)
        link1 = Link(1, 'ALINK', 'INITIATES', instance0, instance1)
        self.assertEqual(link0.link_id, 0)
        self.assertEqual(link0.link_tag, 'ALINK')
        self.assertEqual(link0.rel_type, 'INITIATES')
        self.assertTrue(isinstance(link0.start_node, TimeX))
        self.assertTrue(isinstance(link0.related_to_node, TimeX))
        self.assertTrue(isinstance(link1.start_node, Instance))
        self.assertTrue(isinstance(link1.related_to_node, Instance))

    def test_non_default(self):
        link2 = Link(0, 'ALINK', 'INITIATES', timex0, timex1, signal, 'USER', 'syntax')
        self.assertEqual(link2.signal, signal)
        self.assertEqual(link2.origin_type, 'USER')
        self.assertEqual(link2.syntax, 'syntax')

    def test_exceptions(self):
        with self.assertRaises(Exception):  # Link ID is less than 0
            Link(-1, 'ALINK', 'INITIATES', timex0, timex1)

        with self.assertRaises(Exception):  # Link Tag is invalid
            Link(0, 'LINK', 'INITIATES', timex0, timex1)

        with self.assertRaises(Exception):  # start_node cannot be none
            Link(0, 'ALINK', 'INITIATES', None, timex1)

        with self.assertRaises(Exception):  # related_to_node cannot be none
            Link(0, 'ALINK', 'INITIATES', timex0, None)

        with self.assertRaises(Exception):  # start_node cannot be Event
            Link(0, 'ALINK', 'INITIATES', event0, timex1)

        with self.assertRaises(Exception):  # related_to_node cannot be Event
            Link(0, 'ALINK', 'INITIATES', timex0, event1)

    def test_invalid_link_tags(self):
        with self.assertRaises(Exception):  # origin_type is invalid
            Link(0, 'TLINK', 'BEFORE', timex0, timex1, origin_type='Invalid')

        with self.assertRaises(Exception):  # wrong tlink type
            Link(0, 'ALINK', 'BEFORE', timex0, timex1)

        with self.assertRaises(Exception):  # wrong tlink type
            Link(0, 'SLINK', 'INITIATES', timex0, timex1)

        with self.assertRaises(Exception):  # wrong tlink type
            Link(0, 'TLINK', 'INITIATES', timex0, timex1)

    # test get_id_str(self)
    # -> for valid links
    def test_get_id_str(self):
        valid = Link(0, 'ALINK', 'INITIATES', timex0, timex1)

        # assert correct id_str
        self.assertEqual(valid.get_id_str(), 'l' + str(valid.link_id))

    # test __hash__(self)
    # -> correct hash
    def test___hash__(self):
        valid = Link(10, 'ALINK', 'INITIATES', timex0, timex1)

        # assert correct hash
        self.assertEqual(valid.__hash__(), hash(str(valid.link_id) + valid.link_tag))

    # test to_json(self)
    def test_to_json(self):
        valid = Link(10, 'ALINK', 'INITIATES', timex0, timex1)

        sig = valid.signal.to_json() if valid.signal is not None else "\"NULL\""
        origin_t = valid.origin_type if valid.origin_type is not None else "NULL"
        syntax = valid.syntax if valid.syntax is not None else "NULL"

        # match the content of to_json to the content returned by link.to_json
        self.assertEqual(valid.to_json(), str(f'{{"id":"{valid.get_id_str()}", '
                                              f'"tag":"{valid.link_tag}", '
                                              f'"rel_type":"{valid.rel_type}", '
                                              f'"eventInstance":"{valid.start_node.get_id_str()}", '
                                              f'"relatedToNode":"{valid.related_to_node.get_id_str()}", '
                                              f'"signal":{sig}, '
                                              f'"origin_type":"{origin_t}", '
                                              f'"syntax":"{syntax}"}}'))


if __name__ == '__main__':
    unittest.main()
