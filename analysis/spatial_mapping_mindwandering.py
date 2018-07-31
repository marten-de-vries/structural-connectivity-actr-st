import heapq
import math

from .data.fox import source_rois
from .data.nkirockland import xyz as target_rois, labels

result = []
for name, (roi_x, roi_y, roi_z) in source_rois.items():
    for i, ((x, y, z), region) in enumerate(zip(target_rois, labels)):
        # find closest (spatial) matches between ACT-R ROIs and DTI regions
        distance = math.sqrt(
            (x - roi_x) ** 2 +
            (y - roi_y) ** 2 +
            (z - roi_z) ** 2)
        heapq.heappush(result, (distance, i, name, region))

if __name__ == '__main__':
    encountered = set()
    while result:
        item = heapq.heappop(result)
        name = item[2]
        first = '*' if name not in encountered else ''
        encountered.add(name)
        print(first, item)
