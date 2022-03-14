# edited by gparr014

import unittest
import os
from pytlex_core import IndeterminacyDetector, Graph, Link
from pytlex_tests import Testing_utilities


class IndeterminacyDetectorTest(unittest.TestCase):
    # test each individual method
    def test_solve(self):
        # test null graph and empty graphs
        with self.assertRaises(Exception):
            g = Graph.Graph(None, None, None, None)
            IndeterminacyDetector.solve(g)
        with self.assertRaises(Exception):
            g = None
            IndeterminacyDetector.solve(g)

        # for score, Indeterminant time points, and Indeterminant sections
        # we will be using wsj_0167.tml with the following results:
        # score: 0.8571428571428571
        # indeterminant points > BELOW
        # total time points {'2', '3', '1', '6', '4', '5'}
        g = Graph.Graph(None, None, r"../pytlex_data/TimeBankCorpus/wsj_0167.tml", None)
        score, i_time_points, t_time_points = IndeterminacyDetector.solve(g)

        # test score
        self.assertEqual(score, 0.8571428571428571)

        # test indeterminant time points
        i_points = {'eiid2090_minus',
                    'eiid2091_minus',
                    'eiid2091_plus',
                    'eiid2092_minus',
                    'eiid2092_plus',
                    'eiid2093_minus',
                    'eiid2093_plus',
                    'eiid2096_minus',
                    'eiid2096_plus',
                    'eiid2097_minus',
                    'eiid2097_plus',
                    'eiid2098_minus',
                    'eiid2099_minus',
                    'eiid2099_plus',
                    'eiid2100_minus',
                    'eiid2100_plus',
                    'eiid2101_minus',
                    'eiid2101_plus',
                    'eiid2102_minus',
                    'eiid2102_plus',
                    'eiid2103_minus',
                    'eiid2103_plus',
                    'eiid2104_minus',
                    'eiid2104_plus',
                    'eiid2105_minus',
                    'eiid2105_plus',
                    'eiid2106_minus',
                    'eiid2106_plus',
                    't19_minus',
                    't21_minus',
                    't21_plus',
                    't22_minus',
                    't22_plus',
                    't23_minus',
                    't23_plus',
                    't24_minus'}
        self.assertEqual(i_time_points, i_points)

        # test total time points
        time_points = {'2', '3', '1', '6', '4', '5'}
        self.assertEqual(t_time_points, time_points)

        # test the entire corpus now
        # takes 3 min 9 sec
        corpus_path = r'../pytlex_data/TimeBankCorpus'
        corpus_files = [f for _, _, flist in os.walk(corpus_path) for f in flist]

        for file in corpus_files:
            g = Graph.Graph(filepath=corpus_path + '/' + file)
            print(f'{file}\t{g.indeterminacy_score}')

    # test method total_time_points()
    # first with a 2 item list, then 0
    def test_total_time_points(self):
        t_case1 = {"key1": ["s1", "s2"]}
        t_case2 = {}
        self.assertEqual(IndeterminacyDetector.total_time_points(t_case1), 2)
        self.assertEqual(IndeterminacyDetector.total_time_points(t_case2), 0)

    # tests a link between nodes
    def test_link_between(self):
        # manual nodes to test if they are related
        t1 = Testing_utilities.test_timex(1)
        t2 = Testing_utilities.test_timex()
        t3 = Testing_utilities.test_timex()

        l1 = Link.Link(1, "TLINK", "BEFORE", t1, t2)
        l2 = Link.Link(2, "TLINK", "BEFORE", t3, t2)

        test_g = Graph.Graph({t1, t2, t3}, {l1, l2})

        self.assertEqual(IndeterminacyDetector.link_between("t1", "t2", test_g), True)
        self.assertEqual(IndeterminacyDetector.link_between("t1", "t3", test_g), False)

    # solve starting from timepoint1 and timepoint2
    def test_solve_with_new_constraint(self):
        # make a test graph that has 6 links
        t1 = Testing_utilities.test_timex(1)
        t2 = Testing_utilities.test_timex()
        t3 = Testing_utilities.test_timex()
        t4 = Testing_utilities.test_timex()
        t5 = Testing_utilities.test_timex()
        t6 = Testing_utilities.test_timex()

        l1 = Link.Link(1, "TLINK", "BEFORE", t1, t2)
        l2 = Link.Link(2, "TLINK", "BEFORE", t3, t2)
        l3 = Link.Link(3, "TLINK", "BEGUN_BY", t4, t3)
        l4 = Link.Link(4, "TLINK", "BEFORE", t4, t5)
        l5 = Link.Link(5, "TLINK", "INCLUDES", t5, t6)

        test_g = Graph.Graph({t1, t2, t3, t4, t5, t6}, {l1, l2, l3, l4, l5})

        # if the graph is None, make sure the exception is caught
        with self.assertRaises(Exception):
            IndeterminacyDetector.solve_with_new_constraint(None, False, "t1", "t2")

        # test empty starting points
        with self.assertRaises(Exception):
            IndeterminacyDetector.solve_with_new_constraint(test_g, False, "", "")

        # if timepoint1 == timepoint2, it should return True
        self.assertEqual(IndeterminacyDetector.solve_with_new_constraint(test_g, True, "t1", "t1"), True)

        # if timepoint1 != timepoint2 and flag is False return True
        self.assertEqual(IndeterminacyDetector.solve_with_new_constraint(test_g, False, "t1", "t2"), True)


if __name__ == '__main__':
    unittest.main()
