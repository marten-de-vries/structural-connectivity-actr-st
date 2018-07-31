import matplotlib.pyplot as plt
import bct
from .utils.distribution import plot_distribution
from .utils.ui import generate_plots


SEED = 3040994943


def process(data):
    ci, q = bct.community_louvain(data, gamma=1, B='modularity', seed=SEED)
    return ci  # TODO: report q?


def plot(result, name):
    plot_distribution(result, name)
    plt.ylabel("TODO (measure of connectivity)")


if __name__ == '__main__':
    generate_plots(process, plot,
                   "TODO of brain regions for subject #%s",
                   'community_louvain_%s')
