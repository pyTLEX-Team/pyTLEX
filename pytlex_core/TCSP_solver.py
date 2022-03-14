import json
import time
from typing import Optional

import constraint

# a ended before b started
def BEFORE(a_plus, b_minus):
    if a_plus < b_minus:
        return True

# b ended before a started
def AFTER(b_plus, a_minus):
    if b_plus < a_minus:
        return True

# b starts immediately as a ends
def IBEFORE(a_plus, b_minus):
    if a_plus == b_minus:
        return True

# a starts immediately as b ends
def IAFTER(b_plus, a_minus):
    if b_plus == a_minus:
        return True

# Both a and b begin at the same time, but a ends before b
def BEGINS(a_minus, b_minus, a_plus, b_plus):
    if a_minus == b_minus and a_plus < b_plus:
        return True

# Both a and b begin at the same time, but b ends before a
def BEGUN_BY(a_minus, b_minus, a_plus, b_plus):
    if a_minus == b_minus and b_plus < a_plus:
        return True

# b starts before a, but both end at the same time
def ENDS(a_minus, b_minus, a_plus, b_plus):
    if b_minus < a_minus and a_plus == b_plus:
        return True

# a starts before b, but both end at the same time
def ENDED_BY(a_minus, b_minus, a_plus, b_plus):
    if a_minus < b_minus and b_plus == a_plus:
        return True

# both a and b start together, and end together
def DURING(a_minus, b_minus, a_plus, b_plus):
    if b_minus == a_minus and a_plus == b_plus:
        return True

# both b and a start together, and end together
def DURING_INV(a_minus, b_minus, a_plus, b_plus):
    if a_minus == b_minus and b_plus == a_plus:
        return True

# a starts before b, and b ends before a
def INCLUDES(a_minus, b_minus, a_plus, b_plus):
    if a_minus < b_minus and b_plus < a_plus:
        return True

# b starts before a, and a ends before b
def IS_INCLUDED(a_minus, b_minus, a_plus, b_plus):
    if b_minus < a_minus and a_plus < b_plus:
        return True

# both a and b start together, and end together
def SIMULTANEOUS(a_minus, b_minus, a_plus, b_plus):
    if a_minus == b_minus and a_plus == b_plus:
        return True

# both a and b start together, and end together
def IDENTITY(a_minus, b_minus, a_plus, b_plus):
    if a_minus == b_minus and a_plus == b_plus:
        return True


"""
@:arg graph, partitioned graph whose timeline is to be found
@:arg single, determines whether only a single solution is expected, optional attribute, default is True
@:arg condense, if set to True, formats timeline to show all events at each point
                if set to False, formats timeline to show time point for each event
                optional attribute, default is True
@:returns list of dicts, representing a timeline for the graph
"""
def solve(graph, single: Optional[bool] = True, condense: Optional[bool] = True) -> list[dict[str, list[str]]]:
    list_of_tuples = []

    # deal w/ singletons
    if len(graph.links) == 0:
        out = {}
        for node in graph.nodes:
            out[1] = node.get_id_str()+"_minus"
            out[2] = node.get_id_str()+"_plus"
        return out

    for link in graph.links:
        if link.link_tag == "SLINK":
            raise Exception("S-Link found while trying to compute timeline. Graph is not properly partitioned.", graph)
        list_of_tuples.append((link.start_node.get_id_str(), link.rel_type, link.related_to_node.get_id_str()))

    i = 2
    solutions = None
    number_of_nodes = 0

    node_set = set()
    for a, link_tag, b in list_of_tuples:

        if a not in node_set:
            node_set.add(a)
            number_of_nodes += 1

        if b not in node_set:
            node_set.add(b)
            number_of_nodes += 1

    while (solutions is None or len(solutions) == 0) and i <= (number_of_nodes * 2) + 1:
        problem = constraint.Problem()
        node_set = set()

        for a, link_tag, b in list_of_tuples:

            if a not in node_set:
                problem.addVariable(a + '_minus', range(1, i))
                problem.addVariable(a + '_plus', range(1, i))
                problem.addConstraint(BEFORE, [a + "_minus", a + "_plus"])
                node_set.add(a)

            if b not in node_set:
                problem.addVariable(b + '_minus', range(1, i))
                problem.addVariable(b + '_plus', range(1, i))
                problem.addConstraint(BEFORE, [b + "_minus", b + "_plus"])
                node_set.add(b)

            if link_tag == 'BEFORE':
                problem.addConstraint(BEFORE, [a + '_plus', b + '_minus'])
            elif link_tag == 'AFTER':
                problem.addConstraint(AFTER, [b + '_plus', a + '_minus'])
            elif link_tag == 'IBEFORE':
                problem.addConstraint(IBEFORE, [a + '_plus', b + '_minus'])
            elif link_tag == 'IAFTER':
                problem.addConstraint(IAFTER, [b + '_plus', a + '_minus'])
            elif link_tag == 'BEGINS' or link_tag == 'INITIATES':
                problem.addConstraint(BEGINS, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            elif link_tag == 'BEGUN_BY':
                problem.addConstraint(BEGUN_BY, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            elif link_tag == 'ENDS' or link_tag == 'CULMINATES' or link_tag == 'TERMINATES':
                problem.addConstraint(ENDS, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            elif link_tag == 'ENDED_BY':
                problem.addConstraint(ENDED_BY, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            elif link_tag == 'DURING':
                problem.addConstraint(DURING, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            elif link_tag == 'DURING_INV':
                problem.addConstraint(DURING_INV, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            elif link_tag == 'INCLUDES':
                problem.addConstraint(INCLUDES, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            elif link_tag == 'IS_INCLUDED' or link_tag == 'CONTINUES' or link_tag == 'REINITIATES':
                problem.addConstraint(IS_INCLUDED, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            elif link_tag == 'SIMULTANEOUS':
                problem.addConstraint(SIMULTANEOUS, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            elif link_tag == 'IDENTITY':
                problem.addConstraint(IDENTITY, [a + '_minus', b + '_minus', a + '_plus', b + '_plus'])
            else :
                err = "Invalid relation type for node"
                raise TypeError(err)

        if single:
            solutions = problem.getSolution()
        else:
            solutions = problem.getSolutions()

        i += 1
        # print(i)

    if single:
        if solutions is None:
            solutions = []
        else:
            solutions = [solutions]

    if condense:
        return format_condensed(solutions)
    else:
        return solutions


"""
@:arg uncondensed dictionary, crafted by solve()
@:returns condensed dict
"""
def format_condensed(solution_list):
    if solution_list is None:
        return None

    temp_list = []

    for solution in solution_list:
        if not isinstance(solution,dict) :
            err = "Expected a list of dict()"
            raise TypeError(err)
        for key in solution.copy():
            if not isinstance(key, str):
                err = "Expected dict() key to be of type string"
                raise TypeError(err)
            value = solution[key]
            if value in solution:
                solution[value].append(key)

            else:
                solution[value] = [key]

            del solution[key]

        temp_list.append({j: k for j, k in solution.items()})

    ret = []
    for solution in temp_list:
        temp_solution = {}
        for i in range(1, len(solution)+1):
            temp_solution[int(i)] = solution[i]
        ret.append(temp_solution)

    return ret


