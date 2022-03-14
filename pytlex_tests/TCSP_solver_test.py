import unittest
from pytlex_core import TCSP_solver
from pytlex_core.Graph import Graph
from pytlex_core.Partitioner import partition_graph
from pytlex_tests import Testing_utilities

"""
Error testing for TCSP_solver.py from core
This file tests each method of TCSP_solver including absurd input

Last updated by: iparr011
"""


class TCSPTestCase(unittest.TestCase):

    # Test each of the time based methods
    def test_spacetime(self):
        # Testing BEFORE
        self.assertTrue(TCSP_solver.BEFORE('a','b'))
        self.assertTrue(TCSP_solver.BEFORE(1,2))
        self.assertTrue(TCSP_solver.BEFORE("Hel","Help"))
        # Testing AFTER
        self.assertTrue(TCSP_solver.AFTER('a', 'b'))
        self.assertTrue(TCSP_solver.AFTER(1, 2))
        self.assertTrue(TCSP_solver.AFTER("Hel", "Help"))
        # Testing IBEFORE
        self.assertTrue(TCSP_solver.IBEFORE('a', 'a'))
        self.assertTrue(TCSP_solver.IBEFORE(0, 0))
        self.assertTrue(TCSP_solver.IBEFORE("Hello", "Hello"))
        # Testing IAFTER
        self.assertTrue(TCSP_solver.IAFTER('a', 'a'))
        self.assertTrue(TCSP_solver.IAFTER(0, 0))
        self.assertTrue(TCSP_solver.IAFTER("Hello", "Hello"))
        # Testing BEGINS
        self.assertTrue(TCSP_solver.BEGINS('a', 'a', 'b', 'c'))
        self.assertTrue(TCSP_solver.BEGINS(1, 1, 2, 371987389))
        self.assertTrue(TCSP_solver.BEGINS('H', 'H', 'He', 'Hello Mario'))
        # Testing BEGUN_BY
        self.assertTrue(TCSP_solver.BEGUN_BY('a', 'a', 'c', 'b'))
        self.assertTrue(TCSP_solver.BEGUN_BY(1, 1, 2, -90))
        self.assertTrue(TCSP_solver.BEGUN_BY('H', 'H', 'Helium', 'He'))
        # Testing ENDS
        self.assertTrue(TCSP_solver.ENDS('b', 'a', 'c', 'c'))
        self.assertTrue(TCSP_solver.ENDS(3, 1, -1, -1))
        self.assertTrue(TCSP_solver.ENDS('Heyo', 'Hey', 'Helium', 'Helium'))
        # Testing ENDED_BY
        self.assertTrue(TCSP_solver.ENDED_BY('a', 'z', 'c', 'c'))
        self.assertTrue(TCSP_solver.ENDED_BY(0, 1, -1, -1))
        self.assertTrue(TCSP_solver.ENDED_BY('He', 'Hey', 'Helium', 'Helium'))
        # Testing DURING
        self.assertTrue(TCSP_solver.DURING('z', 'z', 'c', 'c'))
        self.assertTrue(TCSP_solver.DURING(0, 0, -1, -1))
        self.assertTrue(TCSP_solver.DURING('Hee', 'Hee', 'Helium', 'Helium'))
        # Testing DURING_INV
        self.assertTrue(TCSP_solver.DURING_INV('z', 'z', 'c', 'c'))
        self.assertTrue(TCSP_solver.DURING_INV(0, 0, -1, -1))
        self.assertTrue(TCSP_solver.DURING_INV('Hee', 'Hee', 'Helium', 'Helium'))
        # Testing INCLUDES
        self.assertTrue(TCSP_solver.INCLUDES('x', 'z', 'd', 'c'))
        self.assertTrue(TCSP_solver.INCLUDES(0, 3, 0, -1))
        self.assertTrue(TCSP_solver.INCLUDES('He', 'Hee', 'Helium', 'He'))
        # Testing IS_INCLUDED
        self.assertTrue(TCSP_solver.IS_INCLUDED('z', 'f', 'c', 'd'))
        self.assertTrue(TCSP_solver.IS_INCLUDED(0, -89, -9, -1))
        self.assertTrue(TCSP_solver.IS_INCLUDED('Hello', 'H', 'Helium', 'Heliumite'))
        # Testing IS_INCLUDED
        self.assertTrue(TCSP_solver.IS_INCLUDED('z', 'f', 'c', 'd'))
        self.assertTrue(TCSP_solver.IS_INCLUDED(0, -89, -9, -1))
        self.assertTrue(TCSP_solver.IS_INCLUDED('Hello', 'H', 'Helium', 'Heliumite'))
        # Testing SIMULTANEOUS
        self.assertTrue(TCSP_solver.SIMULTANEOUS('z', 'z', 'c', 'c'))
        self.assertTrue(TCSP_solver.SIMULTANEOUS(0, 0, -1, -1))
        self.assertTrue(TCSP_solver.SIMULTANEOUS('Hee', 'Hee', 'Helium', 'Helium'))
        # Testing SIMULTANEOUS
        self.assertTrue(TCSP_solver.SIMULTANEOUS('z', 'z', 'c', 'c'))
        self.assertTrue(TCSP_solver.SIMULTANEOUS(0, 0, -1, -1))
        self.assertTrue(TCSP_solver.SIMULTANEOUS('Hee', 'Hee', 'Helium', 'Helium'))
        # Testing IDENTITY
        self.assertTrue(TCSP_solver.IDENTITY('z', 'z', 'c', 'c'))
        self.assertTrue(TCSP_solver.IDENTITY(0, 0, -1, -1))
        self.assertTrue(TCSP_solver.IDENTITY('Hee', 'Hee', 'Helium', 'Helium'))

        # A bit of absurdism never hurt anyone
        with self.assertRaises(Exception):  # Should return true
            TCSP_solver.BEFORE('a', 14)
        with self.assertRaises(Exception):  # Should return true
            TCSP_solver.AFTER("",''+0)
        with self.assertRaises(Exception):  # Should return true
            TCSP_solver.IAFTER('a'+"")
        with self.assertRaises(Exception):  # Should return true
            TCSP_solver.INCLUDES(None,None,True,False)
        with self.assertRaises(Exception):  # Should return true
            TCSP_solver.AFTER(Testing_utilities.consistent_graph_1(),Testing_utilities.consistent_graph_4())

    # Testing main method solve()
    def test_solve(self):
        print()
        # If graph includes a SLINK, should raise an exception
        graph = Testing_utilities.wsj_0006()
        with self.assertRaises(Exception):
            TCSP_solver.solve(graph)
        # If graph has no links, should return dict of ID_minus and ID_plus for a single node
        graph.links = set()
        print("The nodes for this graph are:")
        for node in graph.nodes :
            print(node)
        print("A timeline for this graph is:")
        print(TCSP_solver.solve(graph))
        # If graph has neither link nor nodes, should return an empty dictionary
        graph.nodes = set()
        self.assertEqual(TCSP_solver.solve(graph), {})
        # Otherwise, should return dict of all nodes.
        # Nodes in the dict should be organized from "earliest" to "latest" in increasing integers
        print()
        graph = Testing_utilities.consistent_graph_1()
        print("The nodes for this graph are:")
        for node in graph.nodes :
            print(node)
        print("The links for this graph are:")
        for link in graph.links :
            print(link)
        # Each node has two elements, a minus and plus, where minus happens before plus
        # In our graph, since the only link has type BEFORE, it tells us that the starting node (tID=50)
        # must have happened before the related node (tID=51)
        # Thus, solve() will determine that the plus of the starting node must have happened before the
        # minus of the related node
        print("A timeline for this graph is:")
        print(TCSP_solver.solve(graph))
        test_timeline = [{1: ['t50_minus'], 2: ['t50_plus'], 3: ['t51_minus'], 4: ['t51_plus']}]
        self.assertEqual(TCSP_solver.solve(graph),test_timeline)
        # If we manually set the type to AFTER, then solve() will conclude that the plus of the related
        # node must have happened before the minus of the starting node (50 started after 51 ended)
        for link in graph.links :
            link.rel_type = "AFTER"
        print("Knowing 50 happens after 51, a timeline for this graph is:")
        print(TCSP_solver.solve(graph))
        test_timeline = [{1: ['t51_minus'], 2: ['t51_plus'], 3: ['t50_minus'], 4: ['t50_plus']}]
        self.assertEqual(TCSP_solver.solve(graph), test_timeline)

        print()
        # Let's manually try every possible type and confirm the results
        for link in graph.links :
            link.rel_type = "IBEFORE"
        print("Knowing 50 ends as 51 starts:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "IAFTER"
        print("Knowing 50 starts as 51 ends:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "BEGINS"
        print("Knowing 50 starts as 51 starts, but 50 ends before 51 ends:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "BEGUN_BY"
        print("Knowing 50 starts as 51 starts, but 51 ends before 50 ends:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "ENDS"
        print("Knowing 51 starts before 50 starts, but both end together:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "ENDED_BY"
        print("Knowing 50 starts before 51 starts, but both end together:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "DURING"
        print("Knowing 50 and 51 start together, and end together:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "DURING_INV"
        print("Knowing 51 and 50 start together, and end together:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "INCLUDES"
        print("Knowing 51 begins after 50 starts, then ends before 50 does:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "IS_INCLUDED"
        print("Knowing 50 begins after 51 starts, then ends before 51 does:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "SIMULTANEOUS"
        print("Knowing 51 and 50 start together, and end together:")
        print(TCSP_solver.solve(graph))
        for link in graph.links :
            link.rel_type = "IDENTITY"
        print("Knowing 51 and 50 start together, and end together:")
        print(TCSP_solver.solve(graph))

        print()
        # If given an invalid type, should raise exception
        for link in graph.links :
            link.rel_type = "ANDROMEDA"
        with self.assertRaises(Exception):
            TCSP_solver.solve(graph)
        # If condense is set to False, the result should have the format:
        # [{"ID1": point_in_time, "ID2": point_in_time, ...}]
        for link in graph.links :
            link.rel_type = "IBEFORE"
        print("Knowing 50 ends as 51 starts, and condense set to True:")
        print(TCSP_solver.solve(graph))
        print("Knowing 50 ends as 51 starts, and condense set to False:")
        print(TCSP_solver.solve(graph,True,False))

        # If single is set to False, should return more than a single result
        # I can't seem to find a graph where changing single does anything though,
        # so put a pin on that

        # Note that testing this method on a partitioned inconsistent graph will
        # cause the program to never complete, so dont try that a home kids

    def test_format_condensed(self):
        print()
        # Should format an uncondensed graph into a condensed one
        graph = Testing_utilities.consistent_graph_1()
        results_condensed = TCSP_solver.solve(graph)
        print("Condensed graph, using solve():",results_condensed)
        results_non_condensed = TCSP_solver.solve(graph,True,False)
        print("Uncondensed graph, using solve():",results_non_condensed)
        results_formatted = TCSP_solver.format_condensed(results_non_condensed)
        print("Condensed graph, using format_condensed():",results_formatted)
        self.assertEqual(results_condensed,results_formatted)

        # If given None, should return None
        self.assertEqual(TCSP_solver.format_condensed(None), None)
        # If given an empty list, should return an empty list
        self.assertEqual(TCSP_solver.format_condensed([]), [])
        # If given a list of anything but dictionaries, raise an exception
        results_test = ["0","172981","-1111"]
        with self.assertRaises(Exception):  # Should return true
            TCSP_solver.format_condensed(results_test)
        # If dicts includes noncontinuous time points, should raise exception
        results_test = [{'t50_plus': 1, 't51_plus': 4}]
        with self.assertRaises(Exception):  # Should return true
            TCSP_solver.format_condensed(results_test)
        # If keys are not strings, should raise exception
        results_test = [{'t50_plus': 1, 1997: 2}]
        with self.assertRaises(Exception):  # Should return true
            TCSP_solver.format_condensed(results_test)


if __name__ == '__main__':
    unittest.main()
