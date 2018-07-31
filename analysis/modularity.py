# Newman's spectral community detection

import matplotlib.pyplot as plt
import bct
from .utils.distribution import plot_distribution
from .utils.ui import generate_plots
from .utils.misc import memory


@memory.cache
def process(data):
    ci, q = bct.modularity_und(data, gamma=1)
    return ci  # TODO: report q?


def plot(result, name):
    # FIXME: unsuitable
    plot_distribution(result, name)
    plt.ylabel("TODO (measure of connectivity)")


if __name__ == '__main__':
    generate_plots(process, plot,
                   "TODO of brain regions for subject #%s",
                   'modularity_%s')
