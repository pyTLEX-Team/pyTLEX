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
    pMake sure that the links are not of rel_tye SIMULTANEOUS or IDENTITY
    """
    if graph is None:
        raise Exception('Graph cannot be None')

    self_looping_links = set()
    for link in graph.links:
        if __is_self_loop(link):
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


# helper function to create a graph from a link
def __make_graph_from_link(_link: Link) -> Graph:
    g = Graph()

    g.links.add(_link)
    g.nodes.add(_link.start_node)
    g.nodes.add(_link.related_to_node)

    return g


# helper function to add an edge to a graph
def __add_link_to_graph(_edge: Link, _graph: Graph):
    _graph.links.add(_edge)
    _graph.nodes.add(_edge.start_node)
    _graph.nodes.add(_edge.related_to_node)


# helper function to detect if a link is a self loop
def __is_self_loop(link: Link) -> bool:
    return link.start_node == link.related_to_node and link.rel_type != 'SIMULTANEOUS' and link.rel_type != 'IDENTITY'


def generate_self_looping_subgraphs(links: {Link}) -> {Graph}:
    """
    Creates a graph containing only the immediate nodes from a given link.
    """
    if links is None:
        raise Exception('The set of links cannot be None')

    return {__make_graph_from_link(link) for link in links if __is_self_loop(link)}


def __complete_inconsistent_cycle(inconsistent_cycle: Graph, consistent_links: [Link]) -> Graph:
    if not is_consistent(inconsistent_cycle):
        return inconsistent_cycle

    # clone the graph
    subgraph = Graph()
    subgraph.links = {link for link in inconsistent_cycle.links}
    subgraph.nodes = {node for node in inconsistent_cycle.nodes}

    for link in consistent_links:
        __add_link_to_graph(link, subgraph)

        if not is_consistent(subgraph):
            __add_link_to_graph(link, inconsistent_cycle)

            return __complete_inconsistent_cycle(inconsistent_cycle,
                                                 [L for L in consistent_links if L.link_id != link.link_id])

    return None


def generate_inconsistent_subgraphs(graph: Graph) -> set[Graph]:
    """
    Given a TimeML graph with inconsistencies, generate a set of subgraphs
    that contain all the links and nodes involved in the inconsistencies that are
    present on the TimeML graph.
    :rtype: object
    """

    if graph is None:
        raise Exception('Graph cannot be None')

    # verify at least one inconsistency exists.
    if is_consistent(graph):
        return set()  # no inconsistencies in this graph.

    # first generate self looping subgraphs
    inconsistent_subgraphs = generate_self_looping_subgraphs(graph.links)

    sub_graph = Graph()
    sub_graph.nodes = {node for node in graph.nodes}

    # generate links that are not self loops
    links = {link for link in graph.links if not __is_self_loop(link)}

    inconsistent_links = list()
    consistent_links = list()

    # add all links to the subgraph and save their state
    for link in links:
        sub_graph.links.add(link)

        if is_consistent(sub_graph):
            consistent_links.append(link)
        else:
            sub_graph.links.remove(link)
            inconsistent_links.append(link)

    # for each inconsistent link, create an inconsistent cycle
    for inconsistent_link in inconsistent_links:
        inconsistent_cycle = __complete_inconsistent_cycle(__make_graph_from_link(inconsistent_link), consistent_links)

        if inconsistent_cycle is None:
            raise Exception

        inconsistent_subgraphs.add(inconsistent_cycle)

        cycle_links = inconsistent_cycle.links
        cycle_links.remove(inconsistent_link)

        for link in cycle_links:
            shared_cycle = __complete_inconsistent_cycle(__make_graph_from_link(link),
                                                         [L for L in consistent_links if L.link_id != link.link_id])
            if shared_cycle is not None:
                inconsistent_subgraphs.add(shared_cycle)

    return inconsistent_subgraphs

