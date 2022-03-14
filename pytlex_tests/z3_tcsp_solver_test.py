from pytlex_core import Z3_tcsp_solver
from pytlex_core import Graph

import unittest


# Methods to test:
# solve() - sort()

class Z3_Tester:

    tester_graph = Graph.Graph(None, None, "/filepath", None)

    def test_solve(self):
        print(Z3_tcsp_solver.solve(self.tester_graph))


if __name__ == "__main__":
    temp = Z3_Tester()
    temp.test_solve()

