import matplotlib.pyplot as plt
import bct

from .utils.ui import generate_plots
from .utils.misc import memory


@memory.cache
def process(data):
    distances, edge_counts = bct.distance_wei(1 / data)
    return distances


def plot(result, name):
    plt.imshow(result.data)


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Distances for subject #%s",
                   'distance_%s')
