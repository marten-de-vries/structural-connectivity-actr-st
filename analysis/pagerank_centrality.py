import matplotlib.pyplot as plt
import bct
from .utils.distribution import plot_distribution
from .utils.ui import generate_plots


def process(data):
    # use the advised value
    return bct.pagerank_centrality(data, d=0.85)


def plot(result, name):
    plot_distribution(result, name)
    plt.ylabel("Page rank centrality")


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Page rank centrality of brain regions for subject #%s",
                   'pagerankcentrality_%s')
