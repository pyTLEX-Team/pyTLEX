import os
import unittest

from pytlex_tests.jTLEX_Data.jTLEX_Counts import *
from pytlex_tests.Testing_utilities import *
from pytlex_core.Inconsistency_detector import *


class InconsistencyDetectorTest(unittest.TestCase):

    # test detect_self_loop_for_graph()
    # **still needs to be updated to match the results of jTLEX**
    # 4.88 sec runtime
    def test_detect_self_loop_for_graph(self):
        corpus_path = r'../pytlex_data/TimeBankCorpus'
        for file, self_loop_count in jTLEX_self_loops.items():
            print(f'\n{file}: {self_loop_count}')
            g = Graph(filepath=corpus_path+'/'+file)
            self.assertEqual(len(detect_self_loop_for_graph(g)), self_loop_count)

    # test every other file that is not considered self loop
    # this is going to assume that len(detect_self_loop_graph()) == 0
    # takes 3 min
    # unfortunately when creating a new graph, the Indeterminacy detector is ran
    # so this test does not really show an accurate run-time on the entire corpus
    # FAILED FILES WSJ900813-0157.tml
    def test_detect_no_self_loops(self):
        corpus_path = r'../pytlex_data/TimeBankCorpus'
        corpus_files_no_self_loops = [res for _, _, f in os.walk(corpus_path)
                                      for res in f
                                      if res not in jTLEX_self_loops.keys()]

        for file in corpus_files_no_self_loops:
            print(file)
            g = Graph(filepath=corpus_path+'/'+file)
            self.assertEqual(len(detect_self_loop_for_graph(g)), 0)

    # test is_consistent() against the inconsistent corpus
    def test_is_inconsistent(self):
        corpus_path = r'../pytlex_data/TimeBankCorpus'
        for f_name in jTLEX_inconsistent_files:
            print(f_name)
            g = Graph(filepath=corpus_path+'/'+f_name)
            self.assertEqual(not g.consistency, not is_consistent(g))

    # test that every graph that is supposed to be consistent, is
    # indeed consistent with the algorithm
    # 2min51sec runtime
    def test_is_consistent(self):
        corpus_path = r'../pytlex_data/TimeBankCorpus'
        corpus_files = [res for _, _, f in os.walk(corpus_path)
                        for res in f
                        if res not in jTLEX_inconsistent_files]

        # test all files that are supposed to be consistent
        for file in corpus_files:
            print(file)
            g = Graph(filepath=corpus_path+'/'+file)
            self.assertEqual(g.consistency, is_consistent(g))

    # compare the results of the pytlex algorithm with jtlex
    # 6 min
    def test_generate_inconsistent_subgraphs_against_jtlex(self):
        corpus_path = r'../pytlex_data/TimeBankCorpus'

        for file, count in jTLEX_inconsistent_subgraphs.items():
            g = Graph(filepath=corpus_path + '/' + file)
            print(f'\n{file}')
            self.assertEqual(len(generate_inconsistent_subgraphs(g)), count)

    # take all files not in the jtlex results
    # 2 min 51 sec
    def test_generate_inconsistent_subg_not_in_jtlex_count(self):
        failed_files = {'VOA19980303.1600.2745.tml'}

        corpus_path = r'../pytlex_data/TimeBankCorpus/'
        corpus_files = [res for _, _, f in os.walk(corpus_path, topdown=True)
                        for res in f
                        if res not in jTLEX_inconsistent_subgraphs.keys()]

        for file in corpus_files:
            if file not in failed_files:
                g = Graph(filepath=corpus_path + file)
                print(f'\n{file}')
                self.assertEqual(len(generate_inconsistent_subgraphs(g)), 0)

    # run the entire corpus and
    # 19 mins
    def test_generate_inconsistent_subgraphs_on_corpus(self):
        corpus_path = r'../pytlex_data/TimeBankCorpus/'
        corpus_files = [res for _, _, f in os.walk(corpus_path, topdown=True)
                        for res in f]

        failed_files = {'VOA19980303.1600.2745.tml'}

        inconsistent_subgraphs_on_corpus = dict()
        count = 0

        for file in corpus_files:
            if file not in failed_files:
                g = Graph(filepath=corpus_path + file)
                res = generate_inconsistent_subgraphs(g)
                subg_count = len(res)
                inconsistent_subgraphs_on_corpus[file] = subg_count

                if subg_count > 0:
                    count += 1
                    print(f'\n{file} has {subg_count} inconsistent sub-graphs\n')

        print(f'Total inconsistent files {count}')
        print(f'Total inconsistent subgraphs: {sum(inconsistent_subgraphs_on_corpus.values())}')

        self.assertEqual(count, 65)


def get_self_loop_dict():
    corpus_path = r'../pytlex_data/TimeBankCorpus'
    corpus = [res for _, _, f in os.walk(corpus_path, topdown=True) for res in f]
    self_loop_dict = {str: int}

    for f in corpus:
        g = Graph(filepath=corpus_path+'/'+f)
        count = len(detect_self_loop_for_graph(g))
        print(f'{f}: {count}')
        self_loop_dict[f] = count

    return self_loop_dict


if __name__ == '__main__':
    unittest.main()
