# Widget for convert graphs Network <--> networkx.Graph
#
# Author - Mael Bervet
# Created on 2019-11-25

import numpy as np
import scipy.sparse as sp
import networkx as nx

from Orange.misc import DistMatrix
from Orange.data import Domain, StringVariable, Table
from Orange.widgets import gui, widget
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
        network = Output("Network", Network)
        graph = Output("Graph", nx.Graph)

    resizing_enabled = False

    class Warning(widget.OWWidget.Warning):
        input_graph_is_none = widget.Msg('Input graph is none')
        input_network_is_none = widget.Msg('Input network is none')


    def __init__(self):
        super().__init__()

        self.outGraph = None
        self.outNetwork = None

        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "Nothing on input yet, waiting to get something.")

    @Inputs.network
    def convert_to_nxGraph(self, network):
        if network is None:
            self.Warning.input_network_is_none()
        else:
            graph = nx.Graph()

            for i in range(network.number_of_nodes()):
                graph.add_node(i, name=i)
    
            for i in range(network.number_of_nodes()):
                for neighbour in network.neighbours(i):
                    graph.add_edge(i, neighbour)
    
            self.outGraph = graph
            self.send_nxGraph()

    @Inputs.graph
    def convet_to_Network(self, graph):
        if graph is None:
            self.Warning.input_graph_is_none()
        else:
            row_data = []
            col_data = []
            data_data = []

            nb_data = len(graph)

            for i in range(nb_data):
                for j in list(graph[i].keys()):
                    data_data.append(1.0)
                    row_data.append(i)
                    col_data.append(j)

            row = np.array(row_data)
            col = np.array(col_data)
            data = np.array(data_data)
            a = sp.csr_matrix((data, (row, col)), shape=(nb_data,nb_data))

            items = Table(Domain([], metas=[StringVariable('label')]), [[i] for i in range(len(graph))])

            self.outNetwork = Network(items, a)
            self.send_Network()

    def send_nxGraph(self):
        self.infoa.setText("Network converted into graph")
        self.Outputs.graph.send(self.outGraph)

    def send_Network(self):
        self.infoa.setText("Graph converted into network")
        self.Outputs.network.send(self.outNetwork)



