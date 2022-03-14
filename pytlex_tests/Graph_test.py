import unittest
import os
from pytlex_core import TCSP_solver
from pytlex_core.Event import Event
from pytlex_core.Graph import Graph,find_timeline,find_total_time_points
from pytlex_core.Instance import Instance
from pytlex_core.Link import Link
from pytlex_core.TimeX import TimeX
from pytlex_tests import Testing_utilities
import json


class Graph_test(unittest.TestCase):
    def test_single(self):
        print("\n")
        for link in Testing_utilities.consistent_graph_2().links:
            print(link)

    def test_non_single(self):
        # Testing on a known .tml file
        print("Filename: wsj_0006")
        filepath = r"../pytlex_data/TimeBankCorpus/wsj_0006.tml"
        graph = Graph(filepath=filepath)

        # Testing to see if graph contains correct number of nodes and links
        self.assertEqual(len(graph.links), 13)
        self.assertEqual(len(graph.nodes), 11)
        # Test if graph is consistent (it should be)
        self.assertTrue(graph.consistency)
        # Test if metadata is identified correctly
        self.assertEqual(len(graph.metadata), 9)
        # Check for raw text
        print(graph.raw_text)

        # Check for nodes in main graph
        nodes_list = list()
        for m_graph in graph.main_graphs :
            for n in m_graph.nodes:
                nodes_list.append(n.get_id_str())
        print("Main graph nodes are:\n",nodes_list)
        # Check for main timeline (should only feature the nodes seen above)
        print("Main timeline is:\n", graph.timeline)
        # Testing timeline methods
        self.assertEqual(graph.get_first_point(), ['eiid75_minus'])
        self.assertEqual(graph.get_last_point(), ['t9_plus'])
        self.assertEqual(graph.get_timeline_length(), 8)
        # self.assertEqual(graph.main_timeline(), graph.timeline)

        # Check for subordinate graphs
        sub_nodes_list = list()
        for sub_graph in graph.subordination_graphs :
            for n in sub_graph.nodes:
                sub_nodes_list.append(n.get_id_str())
        print("Subordination graphs nodes are:\n",sub_nodes_list)
        # Check for subordinate timelines (should only feature the nodes seen above)
        print("Subordinate timelines are:\n", graph.subordinate_timelines())

        # Test get_attachement_points and SLinks
        self.assertEqual(len(graph.get_attachement_points()), len(graph.s_links))
        # Test get_suggested_links
        self.assertEqual(graph.get_suggested_links(), graph.suggested_links)
        # Test to_json
        print("Graph in json format:")
        print(json.dumps(json.loads(graph.to_json()), indent=4, sort_keys=True))

        # Test extra methods
        self.assertEqual(find_timeline(graph), None)
        self.assertEqual(find_total_time_points(graph.timeline), graph.get_total_time_points())

        # If given anything but a formatted tml file/string, should raise an exception
        filepath = r"../pytlex_core/__init__.py"
        with self.assertRaises(Exception):  # Should return true
            bad_graph = Graph(filepath=filepath)

        # It should be able to make a graph out of every .tml file in the corpus without errors
        filepath = r"../pytlex_data/TimeBankCorpus"
        # Dont test UNLESS you have ~4 mins to spare
        # for subdir, dirs, files in os.walk(filepath):
        #     for filename in files:
        #         test_graph = Graph(filepath=(filepath + "/" + filename))


if __name__ == '__main__':
    unittest.main()