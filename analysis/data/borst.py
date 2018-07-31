import os
import pandas

base = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
path = os.path.join(base, 'ACTR-ROIs', 'actrROIs.xls')
data = pandas.read_excel(path, header=2)


def name_for(row):
    return {
        'ACC': 'goal',
        'Parietal': 'imaginal',
        'PFC': 'retrieval',
        'caudate': 'procedural',
        'fusi': 'visual',
        'motor': 'manual',
    }.get(row.region, row.region) + '_' + row.side


talairach_rois = [
    # talairach coordinates
    (name_for(row), row['x'], row['y'], row['z'])
    for _, row in data.iterrows()
]

mni_rois = [
    (name_for(row), row['x.1'], row['y.1'], row['z.1'])
    for _, row in data.iterrows()
]

voxel_sizes = data.iloc[:, 12:15].values
