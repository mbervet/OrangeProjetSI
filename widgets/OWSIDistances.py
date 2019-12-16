# Widget for convert graphs Network <--> networkx.Graph
#
# Author - Yanis Richard - Mael Bervet
# Created on 2019-11-26

import numpy as np

from math import *
from Orange.data import Domain, StringVariable, Table, ContinuousVariable, DiscreteVariable
from Orange.widgets import widget, gui
from Orange.widgets.utils.signals import Input, Output
from Orange.misc import DistMatrix

class OWDistances(widget.OWWidget):
    name = "Distances Discrete/Continuous"
    description = ('Compute distances for input data for numeric and symbolic values. '
                   'All distances are normalized.')
    icon = "icons/Distance.svg"
    priority = 6450

    class Inputs:
        data = Input("Data", Table)

    class Outputs:
        distances = Output("Distances", DistMatrix)

    class Warning(widget.OWWidget.Warning):
        input_data_is_none = widget.Msg('Input graph is none')

    def __init__(self):
        super().__init__()

        self.outDistances = None

    @Inputs.data
    def set_distances(self, data):

        if data is None:
            self.Warning.input_data_is_none()
        else:
            self.outDistances = self.compute_distances(data)
            self.Outputs.distances.send(self.outDistances)

    def compute_distances(self, data):

        nb_data = len(data)
        nb_domain = len(data.domain)
        distances = [[] for _ in range(nb_data)]

        # look for the biggest and the lowest value of each continuous column
        min_max = []
        for i in range(len(data.domain)):
            if isinstance(data.domain[i], ContinuousVariable):
                min_max.append([data[0][data.domain[i]], data[1][data.domain[i]]])
                for j in range(1, nb_data):
                    if data[j][data.domain[i]] < min_max[-1][0]:
                        min_max[-1][0] = data[j][data.domain[i]]
                    if data[j][data.domain[i]] > min_max[-1][1]:
                        min_max[-1][1] = data[j][data.domain[i]]

        # Compute the difference between the biggest and lowest value for each continuous columns
        diff_extrema = [extrema[1] - extrema[0] for extrema in min_max]

        # Compute the distances between each data
        for i in range(nb_data):
            for j in range(i, nb_data):

                sum_continuous_values = 0 # Sum of the squares of the difference of two data for each continuous columns
                sum_discrete_values = 0 # Sum of distances of two points for each discrete columns (0 if equals, 1 else)

                for k in range(len(data.domain)):
                    if isinstance(data.domain[k], ContinuousVariable):
                        sum_continuous_values += ((data[i][data.domain[k]] - data[j][data.domain[k]]) / (diff_extrema[k]))**2
                    else:
                        if data[i][data.domain[k]] != data[j][data.domain[k]]:
                            sum_discrete_values += 1

                sum = (sqrt(sum_continuous_values) + sum_discrete_values) / nb_domain
                distances[i].append(sum)
                if i != j:
                    distances[j].append(sum)

        return DistMatrix(np.array(distances))