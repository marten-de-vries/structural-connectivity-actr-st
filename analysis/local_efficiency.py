import matplotlib.pyplot as plt
import bct

from .utils.distribution import plot_distribution
from .utils.ui import generate_plots
from .utils.misc import memory


@memory.cache
def process(data):
    # average first, then calculate. Because calculation is too slow.
    return bct.efficiency_wei(data, local=True)


def plot(result, name):
    plot_distribution(result, name)
    plt.ylabel("Local efficiency")


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Efficiency of brain regions for subject #%s",
                   'localefficiency_%s')
