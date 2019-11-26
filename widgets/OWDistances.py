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

    def __init__(self):
        super().__init__()

        self.outDistances = None

    @Inputs.data
    def set_distances(self, data):

        minima = []
        maxima = []

        nb_data = len(data)
        nb_domain = len(data.domain)
        distances = [[] for _ in range(nb_data)]

        for domain in data.domain:
            if(isinstance(domain, ContinuousVariable)):
                values = [row[domain] for row in data]
                minima.append(min(values))
                maxima.append(max(values))

        for i in range(nb_data):
            for j in range(i, nb_data):

                sum_continuous_values = 0
                sum_discrete_values = 0
                ite_min_max = 0

                for domain in data.domain:
                    if isinstance(domain, ContinuousVariable):
                        sum_continuous_values = ((data[i][domain] - data[j][domain]) / (maxima[ite_min_max] - minima[ite_min_max]))**2
                        ite_min_max += 1
                    else:
                        if data[i][domain] != data[j][domain]:
                            sum_discrete_values += 1

                sum = (sqrt(sum_continuous_values) + sum_discrete_values) / nb_domain
                distances[i].append(sum)
                distances[j].append(sum)

        self.outDistances = DistMatrix(np.array(list(map(lambda x: [k for k in x], distances))))
        self.Outputs.distances.send(self.outDistances)





