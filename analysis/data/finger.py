"""Finger et al. (2016) data set"""

import scipy.io
import numpy
import os

path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'dti2eeg')

SC = scipy.io.loadmat(os.path.join(path, 'dti', 'SC.mat'))['SC']
labels = scipy.io.loadmat(os.path.join(path, 'labels_sources.mat'))
labels = numpy.array([label[0] for label in labels['labels_sources'][:, 0]])

ids = list(range(1, 18))

actr_mapping = [{
    # left hemisphere:
    2: 'goal',
    6: 'visual',
    20: 'retrieval',
    24: 'manual',  # and vocal
    25: 'imaginal',
    29: 'imaginal',
    30: 'aural',
    # right hemisphere:
    35: 'goal',
    39: 'visual',
    53: 'retrieval',
    57: 'manual',  # and vocal
    58: 'imaginal',
    62: 'imaginal',
    63: 'aural',
}.get(idx + 1) for idx in range(len(labels))]
# +1 to convert from matlab coordinates

# TODO: mind_wandering_mapping

def load_data(participant_id):
    data = SC[:, participant_id - 1][0]
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if y < x:
                if data[x][y] == cell or numpy.isnan(data[x][y]):
                    data[x][y] = cell
                else:
                    raise AssertionError("Data not undirected!")

    data[numpy.isnan(data)] = 0
    data /= numpy.max(data)
    return data
