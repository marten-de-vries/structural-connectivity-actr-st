from mpl_toolkits.mplot3d import proj3d, art3d
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy

from ..data.nkirockland import xyz, labels
from .plot import mappings_for, mappings_to_colors, color_legend

LABELS = {
    'x': 'x (right/left)',
    'y': 'y (front/back)',
    'z': 'z (inferior/superior)'
}


def plot_interactive(mapping, **kwargs):
    fig = plt.figure(figsize=(12, 6.75))
    ax = fig.add_subplot(111, projection='3d')

    x, y, z = xyz.T
    colors = mappings_to_colors(*mappings_for(mapping))
    visualize_3d_data(x, y, z, labels, colors, fig, ax, **kwargs)

    ax.set_xlabel(LABELS['x'])
    ax.set_ylabel(LABELS['y'])
    ax.set_zlabel(LABELS['z'])
    color_legend(mapping)

    draw_eye(ax, -20, 60, -35)
    draw_eye(ax, 20, 60, -35)

    fig.subplots_adjust(left=0, bottom=0, right=1, top=1,
                        wspace=None, hspace=None)

    return fig, ax


# function adapted from:
# DonCristobal (2016, https://stackoverflow.com/a/35231655) which in turn is
# based on HYRY (2012, https://stackoverflow.com/a/10394128)
def visualize_3d_data(x, y, z, labels, c, fig, ax, **kwargs):
    def distance(x_point, y_point, z_point, event):
        # Project 3d data space to 2d data space
        x2, y2, _ = proj3d.proj_transform(x_point, y_point, z_point,
                                          plt.gca().get_proj())
        # Convert 2d data space to 2d screen space
        x3, y3 = ax.transData.transform((x2, y2))

        return numpy.sqrt((x3 - event.x)**2 + (y3 - event.y)**2)

    def calcClosestDatapoint(event):
        distances = [distance(*point, event) for point in zip(x, y, z)]
        return numpy.argmin(distances)

    def annotatePlot(index):
        # If we have previously displayed another label, remove it first
        if hasattr(annotatePlot, 'label'):
            annotatePlot.label.remove()
        # Get data point from array of points X, at position index
        x2, y2, _ = proj3d.proj_transform(x[index], y[index], z[index],
                                          ax.get_proj())
        lbl = plt.annotate(labels[index],
                           xy=(x2, y2), xytext=(-20, 20),
                           textcoords='offset points',
                           ha='right', va='bottom',
                           bbox=dict(boxstyle='round,pad=0.5',
                                     fc='yellow', alpha=0.5),
                           arrowprops=dict(arrowstyle='->',
                                           connectionstyle='arc3,rad=0'))
        annotatePlot.label = lbl
        fig.canvas.draw()

    def onMouseMotion(event):
        closestIndex = calcClosestDatapoint(event)
        annotatePlot(closestIndex)

    ax.scatter(x, y, z, picker=True, c=c, **kwargs)
    axis_equal_3d(ax)
    fig.canvas.mpl_connect('motion_notify_event', onMouseMotion)


def axis_equal_3d(ax):
    # based on: https://stackoverflow.com/a/12905458
    extents = numpy.array([getattr(ax, 'get_%slim' % dim)() for dim in 'xyz'])
    sz = extents[:, 1] - extents[:, 0]
    centers = numpy.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize / 2
    for center, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_%slim' % dim)(center - r, center + r)


def draw_eye(ax, x, y, z):
    # based on: https://matplotlib.org/examples/mplot3d/surface3d_demo2.html

    # eye ball
    u = numpy.linspace(0, 2 * numpy.pi, 10)
    v = numpy.linspace(0, numpy.pi, 10)
    xs = 13 * numpy.outer(numpy.cos(u), numpy.sin(v)) + x
    ys = 10 * numpy.outer(numpy.sin(u), numpy.sin(v)) + y
    zs = 10 * numpy.outer(numpy.ones(numpy.size(u)), numpy.cos(v)) + z
    ax.plot_surface(xs, ys, zs, color='w')

    # iris
    iris = mpatches.Circle((x, z), 4, facecolor='steelblue')
    ax.add_patch(iris)
    art3d.pathpatch_2d_to_3d(iris, z=y + 10, zdir="y")
    # pupil
    pupil = mpatches.Circle((x, z), 2, facecolor='black')
    ax.add_patch(pupil)
    art3d.pathpatch_2d_to_3d(pupil, z=y + 12, zdir="y")


def plot_box(ax, x, y, z, width, height, depth, color):
    xs = numpy.array([x - width / 2, x + width / 2])
    ys = numpy.array([y - height / 2, y + height / 2])
    zs = numpy.array([z - depth / 2, z + depth / 2])

    ax.plot(xs[[0, 1, 1, 0, 0, 0, 0, 0]],
            ys[[0, 0, 1, 1, 1, 0, 0, 1]],
            zs[[0, 0, 0, 0, 1, 1, 0, 0]], c=color)
    ax.plot(xs[[0, 1, 1, 0]],
            ys[[0, 0, 1, 1]],
            zs[[1, 1, 1, 1]], c=color)
    ax.plot(xs[[1, 1]],
            ys[[0, 0]],
            zs[[0, 1]], c=color)
    ax.plot(xs[[1, 1]],
            ys[[1, 1]],
            zs[[0, 1]], c=color)
