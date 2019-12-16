import numpy as np
import scipy.sparse as sp

from AnyQt.QtCore import QLineF, QSize

from Orange.data import Domain, StringVariable, Table
from Orange.misc import DistMatrix
from Orange.widgets import gui, widget, settings
from Orange.widgets.widget import Input, Output, Msg
from orangecontrib.network.network import Network


class OWSIKNNGraph(widget.OWWidget):
    name = "K nearest neighbors graph generator"
    description = ('Constructs Graph object using knn algorithm. '
                   'Nodes from data table are connected only if they '
                   'are neighbors between the nearest and the k\'th nearest')
    icon = "icons/KNNGraph.svg"
    priority = 6440

    class Inputs:
        distances = Input("Distances", DistMatrix)

    class Outputs:
        network = Output("Network", Network)
        distances = Output("Distances", DistMatrix)

        
    include_knn = settings.Setting(False)
    kNN = settings.Setting(2)


    class Warning(widget.OWWidget.Warning):
        kNN_too_large = \
            Msg('kNN is larger than supplied distance matrix dimension. '
                'Using k = {}')
        large_number_of_nodes = \
            Msg('Large number of nodes/edges; performance will be hindered')
        invalid_number_of_items = \
            Msg('Number of data items does not match the nunmber of nodes')

    class Error(widget.OWWidget.Error):
        number_of_edges = Msg('Estimated number of edges is too high ({})')
        input_distances_is_none = Msg('Input graph is none')


    def __init__(self):
        super().__init__

        self.graph = None
        self.graphMatrix = None

        self.pconnected = 0
        self.nedges = 0

        self.add_knn_control()

        boxInfo = gui.widgetBox(self.controlArea, box="Info")
        self.infoa = gui.widgetLabel(boxInfo, "No data loaded.")
        self.infob = gui.widgetLabel(boxInfo, '')
        self.infoc = gui.widgetLabel(boxInfo, '')

        gui.rubber(self.controlArea)

        self.resize(600, 400)


    def add_knn_control(self):
        hbox = gui.widgetBox(self.controlArea, orientation='horizontal')
        knn_cb = gui.checkBox(hbox, self, 'include_knn',
                              label='Include closest neighbors',
                              callback=self.generateGraph)
        knn = gui.spin(hbox, self, "kNN", 1, 1000, 1,
                       orientation='horizontal',
                       callback=self.generateGraph, callbackOnReturn=1, controlWidth=60)
        knn_cb.disables = [knn]
        knn_cb.makeConsistent()


    @Inputs.distances
    def set_network(self, matrix):
        if matrix is None:
            self.Error.input_distances_is_none()
        else:
            self.graphMatrix = matrix
            self.generateGraph()
            self.send_network()
        
        self.send_matrix()

    def generateGraph(self):
        self.Error.clear()
        self.Warning.clear()
        matrix = None

        if self.graphMatrix is None:
            if hasattr(self, "infoa"):
                self.infoa.setText("No data loaded.")
            if hasattr(self, "infob"):
                self.infob.setText("")
            if hasattr(self, "infoc"):
                self.infoc.setText("")
            self.pconnected = 0
            self.nedges = 0
            self.graph = None
            return

        nEdges = len(self.graphMatrix) * self.kNN

        if nEdges > 200000:
            self.graph = None
            self.Error.number_of_edges(nEdges)
        else:
            items = None
            matrix = self.graphMatrix
            if matrix is not None and matrix.row_items is not None:
                row_items = self.graphMatrix.row_items
                if isinstance(row_items, Table):
                    if matrix.axis == 1:
                        items = row_items
                    else:
                        items = [[v.name] for v in row_items.domain.attributes]
                else:
                    items = [[str(x)] for x in self.graphMatrix.row_items]
            if len(items) != self.graphMatrix.shape[0]:
                self.Warning.invalid_number_of_items()
                items = None
            if items is None:
                items = list(range(self.graphMatrix.shape[0]))
            if not isinstance(items, Table):
                items = Table(
                    Domain([], metas=[StringVariable('label')]),
                    items)

            self.Warning.kNN_too_large.clear()
            if self.kNN >= self.graphMatrix.shape[0]:
                self.Warning.kNN_too_large(self.graphMatrix.shape[0] - 1)

            mask = self.graphMatrix
            if self.include_knn:
                mask |= mask.argsort() < self.kNN
            weights = matrix[mask]
            edges = sp.csr_matrix((weights, mask.nonzero()))
            graph = Network(items, edges)

        self.graph = graph

        if graph is None:
            self.pconnected = 0
            self.nedges = 0
        else:
            self.pconnected = self.graph.number_of_nodes()
            self.nedges = self.graph.number_of_edges()
        if hasattr(self, "infoa"):
            self.infoa.setText("Data items on input: %d" % self.graphMatrix.shape[0])
        if hasattr(self, "infob"):
            self.infob.setText("Network nodes: %d (%3.1f%%)" % (self.pconnected,
                self.pconnected / float(self.graphMatrix.shape[0]) * 100))
        if hasattr(self, "infoc"):
            self.infoc.setText("Network edges: %d (%.2f edges/node)" % (
                self.nedges, self.nedges / float(self.pconnected)
                if self.pconnected else 0))

        self.Warning.large_number_of_nodes.clear()
        if self.pconnected > 1000 or self.nedges > 2000:
            self.Warning.large_number_of_nodes()

    def send_matrix(self):
        self.Outputs.distances.send(self.graphMatrix)

    def send_network(self):
        self.Outputs.network.send(self.graph)
