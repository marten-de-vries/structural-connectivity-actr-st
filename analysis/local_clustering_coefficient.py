# local clustering coefficient

import matplotlib.pyplot as plt
import bct
from .utils.distribution import plot_distribution
from .utils.ui import generate_plots


def process(data):
    return bct.clustering_coef_wu(data)


def plot(result, name):
    plot_distribution(result, name)
    plt.ylabel("Clustering coefficient")


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Clustering coefficient of brain regions for subject #%s",
                   'localclusteringcoefficient_%s')
