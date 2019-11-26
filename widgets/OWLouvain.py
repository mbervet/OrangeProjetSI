# Widget for convert graphs Network <--> networkx.Graph
#
# Author - Yanis Richard - Mael Bervet
# Created on 2019-11-25

import numpy

from Orange.data import Domain, StringVariable, Table, DiscreteVariable
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output

import networkx as nx
from community import community_louvain as cl


class OWDataSamplerA(widget.OWWidget):
    name = "Louvain"
    description = "Run louvain clustering over the graph passed as parameter and output a data table with cluster corresponding"
    icon = "icons/LouvainClustering.svg"
    priority = 10

    class Inputs:
        graph = Input("Graph", nx.Graph)

    class Outputs:
        sample = Output("Sampled Data", Table)

    want_main_area = False

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something.")

    @Inputs.graph
    def set_data(self, dataset):
        if dataset is not None:
            # Run louvain
            partition = cl.best_partition(dataset)

            # Create table
            communities = ["C" + str(x) for x in set(partition.values())]
            variable = DiscreteVariable("Community", values=communities)

            domain = Domain([variable])

            clusters = Table(domain, [["C" + str(x)] for x in partition.values()])

            self.infoa.setText("%d clusters found" % (max([x for x in partition.values()])+1))
            sample = clusters
            self.Outputs.sample.send(clusters)
        else:
            self.infoa.setText(
                "No data on input yet, waiting to get something.")
            self.Outputs.sample.send(None)