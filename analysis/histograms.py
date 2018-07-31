# degrees

import matplotlib.pyplot as plt
import numpy
from .utils.ui import generate_plots


def process(data):
    return numpy.ravel(data)


def plot(result, name):
    plt.hist(result.data)


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Histogram of weights for subject #%s",
                   'hist_%s')
