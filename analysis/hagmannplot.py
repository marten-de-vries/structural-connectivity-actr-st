import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

import scipy.io
import numpy

SIMPLIFIED = True

path = "data/DSI_release2_2011.mat"
data = scipy.io.loadmat(path)
xyz = data['roi_xyz_avg']
labels = data['roi_lbls'][0]

result = numpy.zeros((66, 66))
xyz_small = numpy.zeros((66, 3))
for i, row in enumerate(data['CIJ_fbden_average']):
    for j, value in enumerate(row):
        x = labels[i] - 1
        y = labels[j] - 1
        if x != y:
            result[x][y] += value
for region in range(1, 67):
    xyz_small[region - 1] = numpy.mean(xyz[:, labels == region], axis=1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for (x1, y1, z1), row in zip(xyz_small, result):
    for (x2, y2, z2), value in zip(xyz_small, row):
        if value:
            ax.plot(xs=[x1, x2], ys=[y1, y2], zs=[z1, z2],
                    linewidth=numpy.sqrt(value) * 3)
        ax.scatter(x1, y1, z1)

# fig2 = plt.figure()
# ax2 = fig2.add_subplot(111, projection='3d')
#
# for region in range(1, 67):
#     region_coords = xyz[:, labels == region]
#     if SIMPLIFIED:
#         region_coords = numpy.mean(region_coords, axis=1)
#     ax2.scatter(*region_coords)
plt.show()
