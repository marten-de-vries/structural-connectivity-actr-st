# strength

import matplotlib.pyplot as plt
import bct
from .utils.ui import generate_plots
from .utils.distribution import plot_distribution


def process(data):
    return bct.strengths_und(data)


def plot(result, name):
    plot_distribution(result, name)
    plt.ylabel("Strength")


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Strength of brain regions for subject #%s",
                   'strength_%s')
