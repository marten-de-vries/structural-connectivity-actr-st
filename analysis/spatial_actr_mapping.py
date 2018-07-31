import heapq
import math

from .data.borst import voxel_sizes
from .utils.config import DATA_SET

# load data
if DATA_SET == 'hagmann':
    from .data.borst import talairach_rois as source_rois
    from .data.hagmann import xyz as target_rois, labels
elif DATA_SET == 'nkirockland':
    from .data.borst import mni_rois as source_rois
    from .data.nkirockland import xyz as target_rois, labels
else:
    raise ValueError('unknown data set')

result = []
for ((name, roi_x, roi_y, roi_z),
     (v_width, v_height, v_depth)) in zip(source_rois, voxel_sizes):
    for i, ((x, y, z), region) in enumerate(zip(target_rois, labels)):
        # find closest (spatial) matches between ACT-R ROIs and DTI regions
        distance = math.sqrt(
            (x - roi_x) ** 2 +
            (y - roi_y) ** 2 +
            (z - roi_z) ** 2)
        heapq.heappush(result, (distance, i, name, region))

        # check if directly inside voxel
        inside_voxel = all([
            abs(x - roi_x) < v_width / 2,
            abs(y - roi_y) < v_height / 2,
            abs(z - roi_z) < v_depth / 2,
        ])
        if inside_voxel:
            print(i, name, region)

if __name__ == '__main__':
    while result:
        print(heapq.heappop(result))
