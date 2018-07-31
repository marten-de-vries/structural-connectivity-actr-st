import matplotlib.pyplot as plt
import bct
from .utils.distribution import plot_distribution
from .utils.ui import generate_plots
from .utils.misc import memory


@memory.cache
def process(data):
    return bct.betweenness_wei(data)


def plot(result, name):
    plot_distribution(result, name)
    plt.ylabel("Betweenness")


if __name__ == '__main__':
    title = "Node betweenness cenntrality of brain regions for subject #%s"
    generate_plots(process, plot, title, 'betweenness_%s')
