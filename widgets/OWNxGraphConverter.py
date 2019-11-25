# Widget for convert graphs Network <--> networkx.Graph
#
# Author - Mael Bervet
# Created on 2019-11-25

import numpy as np
import scipy.sparse as sp
import networkx as nx

from Orange.misc import DistMatrix
from Orange.widgets import widget
from Orange.widgets.widget import Input, Output
from orangecontrib.network.network import Network

class OWNxGraphConverter(widget.OWWidget):
    name = "Graph converter between Network and Graph"
    description = ('Convert a graph from Network class from Orange package Network'
                   'to a networkx python library graph'
                   'or a graph from networkx python library'
                   'to a Network class from Orange package Network')
    icon = "icons/converter-icon.png"
    priority = 6440

    class Inputs:
        network = Input("Network", Network)
        graph = Input("Graph", nx.Graph)

    class Outputs:
        network = Input("Network", Network)
        graph = Output("Graph", nx.Graph)

    def __init__(self):
        super().__init__()

        self.outGraph = None
        self.outNetwork = None

    @Inputs.network
    def convert_to_nxGraph(self, network):
        graph = nx.Graph()

        for i in range(network.number_of_nodes()):
            graph.add_node(i, name=i)
    
        for i in range(network.number_of_nodes()):
            for neighbour in network.neighbours(i):
                graph.add_edge(i, neighbour)
    
        outGraph = graph
        send_nxGraph()

    @Inputs.graph
    def convet_to_Network(self, graph):


    def send_nxGraph(self):
        self.Outputs.graph.send(self.outGraph)

    def send_Network(self):
        self.Outputs.network.send(self.outNetwork)



