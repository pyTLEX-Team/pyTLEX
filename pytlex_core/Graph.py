from typing import Union, Optional

from pytlex_core import TCSP_solver, TimeMLParser, Partitioner, Z3_tcsp_solver, IndeterminacyDetector
from pytlex_core.TimeX import TimeX
from pytlex_core.Instance import Instance
from pytlex_core.Link import Link


class Graph:
    def __init__(self,
                 nodes: Optional[set[Union[TimeX, Instance]]] = None,
                 links: Optional[set[Link]] = None,
                 filepath: Optional[str] = None,
                 time_ml_string: Optional[str] = None
                 ):
        """
        :param nodes: the nodes to be placed in an empty graph.
        :type nodes: set of TimeXs and Instances
        :param links: the links to be placed in an empty graph.
        :type links: set of Links
        :param str filepath: the path to a TimeML annotated file to be parsed and analyzed.
        :param str time_ml_string: a TimeML annotated string to be analyzed.
        :param file file: an open TimeML file to be parsed and analyzed
        """

        self.nodes = set()
        self.links = set()
        self.raw_text = None
        self.type = "Overview"
        self.timeline = None
        self.consistency = None
        self.total_time_points = 0



        if not (nodes or links or filepath or time_ml_string):
            pass

        elif nodes is not None:
            self.links = links
            self.nodes = nodes

        elif (filepath is not None) or (time_ml_string is not None):
            if filepath:
                with open(filepath) as file:
                    self.time_ml_data = file.read()
            elif time_ml_string:
                self.time_ml_data = time_ml_string

            self.metadata, self.raw_text, self.links, self.nodes = TimeMLParser.parse(self.time_ml_data)

            # partitioner manipulates the node and link sets, so we hold onto these sets for later restoration
            self.prepartitioned_links = self.links.copy()
            self.prepartitioned_nodes = self.nodes.copy()

            temp = Partitioner.partition_graph(self)
            self.main_graphs = temp['main_graphs']
            self.subordination_graphs = temp['subordination_graphs']
            self.s_links = temp['s_links']
            self.suggested_links = temp['suggested_links']

            self.consistency = True

            self.indeterminacy_score, self.indeterminant_time_points, self.indeterminant_sections = IndeterminacyDetector.solve(self)

            for partition in self.main_graphs + self.subordination_graphs:
                find_timeline(partition)
                if partition.timeline is not None:
                    if self.timeline is None or len(partition.timeline) > len(self.timeline):
                        self.timeline = partition.timeline
                    self.total_time_points += find_total_time_points(partition.timeline)
                if not partition.consistency:
                    self.consistency = False

            for graph in self.main_graphs:
                if graph.timeline != self.timeline:
                    self.subordination_graphs.append(graph)
                    self.main_graphs.remove(graph)

            # nodes and links are restored here
            self.nodes = self.prepartitioned_nodes
            self.links = self.prepartitioned_links
            del self.prepartitioned_links
            del self.prepartitioned_nodes

        else:
            raise Exception("Must supply either a TimeML Annotated File or a TimeML annotated string")

    def main_timeline(self):
        return self.timeline()

    def subordinate_timelines(self):
        return [g.timeline for g in self.subordination_graphs]

    def get_total_time_points(self) -> int:
        time_points = 0
        for g in self.main_graphs + self.subordination_graphs:
            if g.timeline is not None:
                for slice in g.timeline.values():
                    time_points += len(slice)
        return time_points

    def get_attachement_points(self) -> list[str]:
        ret = []
        for link in self.s_links:
            ret.append("{} -> {}".format(link.start_node.get_id_str(), link.related_to_node.get_id_str()))
        return ret

    def get_first_point(self):
        return self.timeline['1']

    def get_last_point(self):
        return self.timeline[str(len(self.timeline))]

    def get_timeline_length(self):
        return len(self.timeline)

    def get_suggested_links(self):
        return self.suggested_links

    def to_json(self):
        ret = "{\"nodes\": ["
        for node in self.nodes:
            ret += node.to_json()
            ret += ", "

        ret = ret[:-2]+"], "

        ret += "\"Links\": ["
        for link in self.links:
            ret += link.to_json()
            ret += ", "

        ret = ret[:-2] + "], "

        ret += "\"Partitions\": ["
        for partition in self.main_graphs + self.subordination_graphs:
            ret += "{\"nodeIDs\": ["
            for node in partition.nodes:
                ret += "\""+node.get_id_str()+"\", "
            ret = ret [:-2] + "], "

            ret += "\"linkIDs\": ["
            for link in partition.links:
                ret += "\"" + link.get_id_str() + "\", "
            if len(partition.links) != 0:
                ret = ret[:-2]
            ret += "],"

            ret += "\"Timeline\": ["

            for section, time_points in partition.timeline.items():
                for time_point in time_points:
                    boundary = "-" if str(time_point).split("_")[1] == "minus" else "+"
                    position = int(str(section).strip("'"))
                    id = str(time_point).split("_")[0]
                    ret += "{{\"id\": \"{}\", \"eventBoundary\": \"{}\", \"position\": \"{}\"}},"\
                        .format(id, position, boundary)

            ret = ret[:-2] + "}], "

            ret += "\"isConsistent\": "
            ret += "\"true\"" if partition.consistency else "\"false\""

            ret += "}, "

        ret = ret[:-2] + "], "

        #for graph in inconsistent_subraphs:

        #for indeterminant time pairs:

        return ret[:-2] + "}"


def find_timeline(partition: Graph) -> None:
    partition.timeline = Z3_tcsp_solver.solve(partition)
    partition.consistency = partition.timeline is not None
    return


def find_total_time_points(timeline: dict[int, [str]]) -> int:
    time_points = 0
    for time in timeline.values():
        time_points += len(time)
    return time_points


