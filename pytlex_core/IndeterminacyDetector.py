from z3 import *
from pytlex_core import Graph, Z3_tcsp_solver


# Algorithm to solve the score, indeterminant_time_points, indeterminant_sections
# on a GraphML object that is not None or empty
def solve(graph: Graph):
    if graph is None or len(graph.links) == 0:
        raise Exception("Graph cannot be 'None' or empty")

    shortest_solution = Z3_tcsp_solver.solve(graph)

    if shortest_solution is None:
        return None, None, None

    indeterminant_sections = set()
    indeterminant_time_points = set()

    for section in shortest_solution:
        for i in range(len(shortest_solution[section])):
            for j in range(i + 1, len(shortest_solution[section])):
                time_point1 = shortest_solution[section][i]
                time_point2 = shortest_solution[section][j]
                node1_id = str(time_point1).split("_")[0]
                node2_id = str(time_point2).split("_")[0]

                if not link_between(node1_id, node2_id, graph) and \
                        time_point1 not in indeterminant_time_points and \
                        time_point2 not in indeterminant_time_points:
                    s1 = solve_with_new_constraint(graph, True, time_point1, time_point2)
                    s2 = solve_with_new_constraint(graph, False, time_point1, time_point2)

                    if s1 and s2:
                        indeterminant_sections.add(section)
                        indeterminant_time_points.add(time_point1)
                        indeterminant_time_points.add(time_point2)

    score = len(indeterminant_time_points) / total_time_points(shortest_solution)

    return score, indeterminant_time_points, indeterminant_sections


# find total timepoints in a timeline
def total_time_points(timeline: dict[str, list[str]]) -> int:
    sum = 0
    for section in timeline.items():
        sum += len(section[1])
    return sum


# find a link between nodes
def link_between(node1, node2, graph) -> bool:
    for link in graph.links:
        if (link.start_node.get_id_str() == node1 and link.related_to_node.get_id_str() == node2) or \
                (link.start_node.get_id_str() == node2 and link.related_to_node.get_id_str() == node1):
            return True
    return False


def solve_with_new_constraint(graph: Graph, equal: bool, time_point1: str, time_point2: str):
    if graph is None or time_point1 == "" or time_point2 == "":
        raise Exception("Graph cannot be 'None or have empty starting points.'")

    s = Solver()

    for node in graph.nodes:
        node_minus = Int(node.get_id_str() + "_minus")
        node_plus = Int(node.get_id_str() + "_plus")
        s.add(node_minus < node_plus)
        s.add(node_minus > 0)

    for link in graph.links:
        a_minus = Int(link.start_node.get_id_str() + "_minus")
        a_plus = Int(link.start_node.get_id_str() + "_plus")
        b_minus = Int(link.related_to_node.get_id_str() + "_minus")
        b_plus = Int(link.related_to_node.get_id_str() + "_plus")

        if link.rel_type == "AFTER":
            s.add(b_plus < a_minus)
        elif link.rel_type == "BEFORE":
            s.add(a_plus < b_minus)
        elif link.rel_type == "IBEFORE":
            s.add(a_plus == b_minus)
        elif link.rel_type == "IAFTER":
            s.add(b_plus == a_minus)
        elif link.rel_type in {"BEGINS", "INITIATES"}:
            s.add(a_minus == b_minus)
            s.add(a_plus < b_plus)
        elif link.rel_type == "BEGUN_BY":
            s.add(a_minus == b_minus)
            s.add(b_plus < a_plus)
        elif link.rel_type in {"ENDS", "CULMINATES", "TERMINATES"}:
            s.add(b_minus < a_minus)
            s.add(a_plus == b_plus)
        elif link.rel_type == "ENDED_BY":
            s.add(a_minus < b_minus)
            s.add(a_plus == b_plus)
        elif link.rel_type == "INCLUDES":
            s.add(a_minus < b_minus)
            s.add(b_plus < a_plus)
        elif link.rel_type in {"IS_INCLUDED", "CONTINUES", "REINITIATES"}:
            s.add(b_minus < a_minus)
            s.add(a_plus < b_plus)
        elif link.rel_type in {"SIMULTANEOUS", "IDENTITY", "DURING", "DURING_INV"}:
            s.add(a_minus == b_minus)
            s.add(a_plus == b_plus)

    tp1 = Int(str(time_point1))
    tp2 = Int(str(time_point2))

    if equal:
        s.add(tp1 == tp2)
    else:
        s.add(tp1 != tp2)

    return s.check().r == Z3_L_TRUE

