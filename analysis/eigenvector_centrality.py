import matplotlib.pyplot as plt
import bct
from .utils.distribution import plot_distribution
from .utils.ui import generate_plots
from .utils.misc import memory


@memory.cache
def process(data):
    return bct.eigenvector_centrality_und(data)


def plot(result, name):
    plot_distribution(result, name)
    plt.ylabel("Eigenvector centrality")


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Eigenvector centrality of brain regions for subject #%s",
                   'eigenvectorcentrality_%s')
