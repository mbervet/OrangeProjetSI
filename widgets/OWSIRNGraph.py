# Widget for proximity graphs
#
# Authors - Richard Yanis
# Created on 2018-11-08

import numpy as np
import scipy.sparse as sp
import networkx as nx

from AnyQt.QtCore import QLineF, QSize

from Orange.data import Domain, StringVariable, Table
from Orange.misc import DistMatrix
from Orange.widgets import gui, widget, settings
from Orange.widgets.widget import Input, Output
from orangecontrib.network.network import Network

import pyqtgraph as pg # lib for graphs, used for Histogram


class OWSIRNGraph(widget.OWWidget):
    name = "RNG Graph Generator"
    description = 'Constructs Graph object using RNG algorithm.'
    icon = "icons/RNGIcon.svg"
    priority = 6447

    class Inputs:
        distances = Input("Distances", DistMatrix)

    class Outputs:
        network = Output("Network", Network)
        distances = Output("Distances", DistMatrix)

    resizing_enabled = False

    class Warning(widget.OWWidget.Warning):
        large_number_of_nodes = widget.Msg('Large number of nodes/edges; performance will be hindered')

    class Error(widget.OWWidget.Error):
        number_of_edges = widget.Msg('Estimated number of edges is too high ({})')

    def __init__(self):
        super().__init__()

        # GUI
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(
            box, "No data on input yet, waiting to get something.")

    # Processing distance input
    @Inputs.distances
    def set_matrix(self, data):
        if data is not None:

            nb_data = len(data)
            G = nx.Graph()

            for i in range(nb_data):
                G.add_node(i)

            for i in range(nb_data):
                for j in range(nb_data):
                    add_edge = True
                    k = 0
                    while add_edge and k < nb_data:
                        if i != j and i != k and data[i][k] < data[i][j] and data[j][k] < data[i][j]:
                            add_edge = False
                        k += 1
                    if add_edge:
                        G.add_edge(i, j)

            sum = 0
            for i in range(nb_data):
                sum += len(G[i])

            self.infoa.setText(
                "Average edges per nodes : " + str(sum / nb_data))

            # Transform Graph to network
            row_data = []
            col_data = []
            data_data = []

            for i in range(nb_data):
                for j in list(G[i].keys()):
                    data_data.append(data[i][j])
                    row_data.append(i)
                    col_data.append(j)

            row = np.array(row_data)
            col = np.array(col_data)
            new_data = np.array(data_data)
            new_network = sp.csr_matrix((new_data, (row, col)), shape=(150, 150))

            items = Table(Domain([], metas=[StringVariable('label')]), [[i] for i in range(len(G))])

            # Send results
            self.Outputs.network.send(Network(items, new_network))
            self.Outputs.distances.send(data)
        else:
            self.infoa.setText(
                "No data on input yet, waiting to get something.")
            self.Outputs.network.send(None)
            self.Outputs.distances.send(None)
