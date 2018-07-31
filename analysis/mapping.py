import matplotlib.animation as manimation
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import matplotlib.patches as mpatches
import numpy

import os

from .utils.config import SHOW_3D_REPR, STORE_ANIMATION, OUT_DIR, PAGE_WIDTH
from .utils.plot import (module_to_color, mappings_to_colors, fix_plot_font,
                         mappings_for)
from .utils.plot3d import plot_interactive, plot_box

from .data.fox import source_rois, source_rois_network
from .data.borst import voxel_sizes, mni_rois
from .data.nkirockland import xyz

PLOTS_2D = [
    ('transverse', 131, ('x', 'y')),
    ('saggital', 132, ('y', 'z')),
    ('coronal', 133, ('x', 'z')),
]

LABELS_2D = {
    'x': 'x (left/right)',
    'y': 'y (back/front)',
    'z': 'z (inferior/superior)'
}


def plot_3d(mapping):
    # interactive plot
    fig, ax = plot_interactive(mapping)
    if mapping in ('actr', 'both'):
        roi_info = zip(mni_rois, voxel_sizes)
        for (name, x, y, z), (width, height, depth) in roi_info:
            color = module_to_color(name.split('_')[0])
            plot_box(ax, x, y, z, width, height, depth, color)
    if mapping in ('mw', 'both'):
        roi_xyz = numpy.array(list(source_rois.values())).T
        ax.scatter(*roi_xyz, s=100, color='black', marker='*')

    ax.set_axis_off()

    def update_view(i):
        if i == 360:
            ax.set_axis_on()
        if i > 360:
            i = 360
        ax.azim = (120 + i) % 360
        ax.elev = (i / 360 * 45) - 20

    if STORE_ANIMATION:
        path = os.path.join(OUT_DIR, 'mapping_%s_3d.mp4' % mapping)
        manimation.FuncAnimation(fig, update_view, frames=401, repeat=False,
                                 interval=32).save(path, dpi=1920 / 12)
    update_view(360)


def plot_2d(mapping):
    # 2d plots
    fig2 = plt.figure(figsize=(PAGE_WIDTH, 10))

    for plane, subplot_pos, variables in PLOTS_2D:
        ax2 = fig2.add_subplot(subplot_pos, aspect='equal')
        if mapping in ('actr', 'both'):
            for (name, x, y, z), (width, height, depth) in zip(mni_rois,
                                                               voxel_sizes):
                color = module_to_color(name.split('_')[0])
                pos = [{
                    'x': x - width / 2,
                    'y': y - height / 2,
                    'z': z - depth / 2
                }[var] for var in variables]
                dims = [{
                    'x': width,
                    'y': height,
                    'z': depth
                }[var] for var in variables]
                p = mpatches.Rectangle(pos, *dims, fill=False, edgecolor=color)
                ax2.add_patch(p)

        if mapping in ('mw', 'both'):
            roi_xyz = numpy.array(list(source_rois.values()))
            relevant_roi_xyz = relevant_vars(roi_xyz, variables)
            roi_colors = [module_to_color(n) for n in source_rois_network]
            plt.scatter(*relevant_roi_xyz, s=100, color=roi_colors, marker='*',
                        edgecolors='white', linewidths=0.1)

        relevant_xyz = relevant_vars(xyz, variables)
        colors = mappings_to_colors(*mappings_for(mapping))
        plt.scatter(*relevant_xyz, c=colors, s=10, edgecolors='white',
                    linewidths=0.1)

        plt.title('%s view' % plane)
        plt.xlabel(LABELS_2D[variables[0]])
        plt.ylabel(LABELS_2D[variables[1]])

    fig2.tight_layout()
    fig2.savefig(os.path.join(OUT_DIR, 'mapping_%s_2d.pgf' % mapping),
                 bbox_inches='tight')
    plt.close()


def relevant_vars(xyz, variables):
    x, y, z = xyz.T
    return [{
        'x': x,
        'y': y,
        'z': z,
    }[var] for var in variables]


if __name__ == '__main__':
    fix_plot_font()
    plot_3d(mapping='actr')
    plot_3d(mapping='mw')
    plot_2d(mapping='actr')
    plot_2d(mapping='mw')
    if SHOW_3D_REPR:
        plt.show()
