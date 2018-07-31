# degree

import matplotlib.pyplot as plt
import bct
from .utils.distribution import plot_distribution
from .utils.ui import generate_plots


def process(data):
    return bct.degrees_und(data)


def plot(result, name):
    plot_distribution(result, name)
    plt.ylabel("Degree")


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Degree of brain regions for subject #%s",
                   'degree_%s')
