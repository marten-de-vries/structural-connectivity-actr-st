import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import matplotlib.cm as mcm

import copy

from .utils.ui import generate_plots
from .utils.config import SHOW_3D_REPR
from .utils.plot3d import plot_interactive


def process(data):
    return data


def plot(result, name):
    if SHOW_3D_REPR:
        from .data.nkirockland import xyz
        fig, ax = plot_interactive(mapping='none')
        for i, row in enumerate(result.data):
            for j, weight in enumerate(row):
                if i < j:
                    if weight < 10**-2:
                        # not worth showing
                        continue
                    ax.plot(*xyz[[i, j]].T, linewidth=weight, c='black')
        ax.azim = 120
        ax.elev = 25
        ax.set_axis_off()
        plt.show()
    cmap = copy.copy(mcm.get_cmap('viridis'))
    cmap.set_bad((0, 0, 0))
    plt.imshow(result.data, norm=mcolors.LogNorm(), cmap=cmap)
    plt.colorbar()


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Connectivity matrix for subject #%s",
                   'matrix_%s')
