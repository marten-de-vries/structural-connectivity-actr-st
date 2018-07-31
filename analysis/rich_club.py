import matplotlib.pyplot as plt
import bct
import numpy
from .utils.ui import generate_plots


def process(data):
    return bct.rich_club_wu(data)


def plot(result, name):
    low, high = 0, 0
    for subject_data in result.raw_data:
        x = numpy.linspace(0, 1, len(subject_data))
        plt.plot(x, subject_data)
        last = -1
        while numpy.isnan(subject_data[last]):
            last -= 1
        if subject_data[last] > 0.5:
            high += 1
        else:
            low += 1
    plt.xlabel("Level (degree)")
    plt.ylabel("Rich club coefficient")
    print('High: %s, low: %s' % (high, low))


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Rich club coefficients for subject #%s",
                   'richclub_%s')
