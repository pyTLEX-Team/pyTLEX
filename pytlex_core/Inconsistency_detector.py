"""
Provides methods for identifying inconsistent subgraphs.

A TimeML graph might not be solvable when formulated as a TCSP because of inconsistencies
in the graph. Among these inconsistencies we find self loops, 2 nodes inconsistencies etc.
InconsistencyDetector provide static methods to verify the consistency of a graph and also,
in the case of inconsistencies, generate the subgraphs of inconsistencies.
**
"""
from pytlex_core import Z3_tcsp_solver
from pytlex_core.Graph import Graph
from pytlex_core.Link import Link


def detect_self_loop_for_graph(graph: Graph) -> set[Link]:
    """
    Traverses through the links in a graph and returns a
    set of any links that self-loop.
    Make sure that the links are not of rel_type SIMULTANEOUS or IDENTITY
    """
    if graph is None:
        raise Exception('Graph cannot be None')

    self_looping_links = set()
    for link in graph.links:
        if link.start_node == link.related_to_node and link.rel_type != 'SIMULTANEOUS' and link.rel_type != 'IDENTITY':
            self_looping_links.add(link)
    return self_looping_links


def is_consistent(graph: Graph) -> bool:
    """
    A static method to verify the consistency of a graph. This is done by trying to solve
    the TCSP presented by the graphs links and nodes. If there is a solution to the TCSP
    then the graph is consistent, otherwise is inconsistent.

    **UPDATED to use Z3_tcsp_solver instead of TCSP_solver**
    """

    if graph is None:
        raise Exception('Graph cannot be None')

    solution = Z3_tcsp_solver.solve(graph)
    if solution is None:
        return False
    return len(solution) != 0


def generate_inconsistent_subgraphs(graph: Graph) -> set[Graph]:
    """
    Given a TimeML graph with inconsistencies, generate a set of subgraphs
    that contain all the links and nodes involved in the inconsistencies that are
    present on the TimeML graph.
    """

    # verify at least one inconsistency exists.
    if is_consistent(graph):
        return None  # no inconsistencies in this graph.

    consistent_links = []
    inconsistent_links = []

    links = graph.links
    nodes = graph.nodes

    sub_graph = Graph()
    for node in nodes:
        sub_graph.nodes.add(node)

    for link in links:
        sub_graph.links.add(link)
        consistent_links.append(link)

        if not is_consistent(sub_graph):
            consistent_links.remove(link)
            inconsistent_links.append(link)
            sub_graph.links.remove(link)

    # find all other links in each inconsistent subgraph
    inconsistent_subgraphs = set()
    for i_link in inconsistent_links:
        inconsistent_subgraph = Graph()
        inconsistent_subgraph.links.add(i_link)
        inconsistent_subgraph.nodes.add(i_link.start_node)
        inconsistent_subgraph.nodes.add(i_link.related_to_node)

        # fix this inconsistent link in the graph
        sub_graph.links.add(i_link)

        consistent_links.append(i_link)
        # test if the graph becomes consistent by removing one link at a time
        for c_link in consistent_links:
            if c_link == i_link:
                continue
            sub_graph.links.remove(c_link)
            if is_consistent(sub_graph):
                # this c_link is an inconsistent link
                inconsistent_subgraph.nodes.add(c_link.start_node)
                inconsistent_subgraph.nodes.add(c_link.related_to_node)
                inconsistent_subgraph.links.add(c_link)
            sub_graph.links.add(c_link)
        sub_graph.links.remove(i_link)
        inconsistent_subgraphs.add(inconsistent_subgraph)
        consistent_links.remove(i_link)
    # print(inconsistent_subgraphs)
    return inconsistent_subgraphs
