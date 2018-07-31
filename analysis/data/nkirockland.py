"""NKI Rockland data set"""

import os
import itertools
import numpy
from ..utils.config import (MERGE_AREAS_WITH_EQUAL_NAME,
                            STATISTICAL_VALIDITY_CHECK)

path = os.path.join(os.path.dirname(__file__),
                    '..', '..', 'data', 'NKI_Rockland')


def read_labels(name):
    with open(os.path.join(path, name)) as f:
        return [label.strip() for label in f if label.strip()]


labels = numpy.array(read_labels('NKI_dti_avg_region_names_full_file.txt'))


# Mappings try to match Borst et al. (2015) ACT-R ROIs. Mostly based on:
#
# - python -m analysis.spatial_act_r_mapping (direct matches + distances)
# - python -m analysis.3d
#
# ... and theory. Distances between the ROI center and the region center are
# given (in MNI space) between brackets.

actr_mapping = numpy.array([{
    # motor (direct matches):
    109: 'manual',  # Right postcentral gyrus (6.2)
    103: 'manual',  # Left postcentral gyrus (6.7)

    # goal:
    # 'Right' anterior cingulate cortex (7.2); see analysis.accright for why
    # this also covers the left hemisphere of the brain sufficiently. Direct
    # match.
    117: 'goal',
    #
    # 'Left Cingulate anterior' is spatially very doubtful. (32.8!)
    #
    # Alternatives (explore if time left):
    # - 90 (Right Cingulate anterior; 16.6)
    # - 7 (Right Juxtapositional Lobule; supplementary motor area; 19.1)
    # - 96 (Left Superior Frontal; 21.2)

    # imaginal (direct matches):
    136: 'imaginal',  # Right Lateral Occipital superior sulcus (6.0)
    79:  'imaginal',  # Left Lateral Occipital superior sulcus (9.9)

    # retrieval:
    41: 'retrieval',  # Right middle frontal gyrus (8.7; direct match)
    52: 'retrieval',  # Left middle frontal gyrus (4.8; direct match)
    78: 'retrieval',  # Right hippocampus (57.5)
    63: 'retrieval',  # Left Hippocampus: (59.7)
    # alternatives: Right Precentral, Right Inferior Frontal pars
    # triangularis, Left Inferior Frontal pars triangularis, Left Precentral

    # aural:
    61:  'aural',  # Right Superior Temporal posterior gyrus (11.5; direct
                   # match)
    # (no equal-named left side area exists)
    28:  'aural',  # Left Insular (10.7); closest
    177: 'aural',  # Left Planum Temporale (11.0); ~ Wernicke's area and
                   # relatively symmetric with right superior temporal
                   # posterior gyrus

    # visual
    77:  'visual',  # Right Lateral Occipital inferior (12.1); direct match
    156: 'visual',  # Left Occipital Fusiform (11.0)
    161: 'visual',  # Right Temporal Occipital Fusiform (11.7)
    119: 'visual',  # Left Inferior Temporal temporooccipital (13.8)

    # procedural:
    # - Basal Ganglia:
    12:  'procedural',  # Right Caudate (7.7)
    18:  'procedural',  # Left Caudate (10.0)
    75:  'procedural',  # Left Putamen (9.0)
    33:  'procedural',  # Right Putamen (9.4)
    #  - Thalamus - there are closer regions, but it's interesting as it is
    #    (commonly assumed to) actually project widely, with the basal ganglia
    #    inhibiting it.
    81:  'procedural',  # Right Thalamus (23.7)
    162: 'procedural',  # Left Thalamus (25.1)
    32:  'procedural',  # Right Thalamus (39.5)
    19:  'procedural',  # Left Thalamus (39.2)

    # vocal
    97: 'vocal',  # Left Precentral (9.9)
    42: 'vocal',  # Right Postcentral (12.5)
}.get(i) for i in range(len(labels))])


mind_wandering_mapping = numpy.array([{
    # 'R lateral prefrontal cortex' -> 'Right Frontal Pole' (distance: 4.7
    # millimeters in MNI space)
    3: 'FPCN',
    # 'L parahippocampus' -> 'Left Parahippocampal posterior' (6.8)
    123: 'DN',
    # 'L mid insula/superior temporal gyrus' -> 'Left Insular' (7.1)
    88: 'other',
    # 'Dorsal anterior cingulate cortex' -> 'Right Cingulate anterior' (8.0)
    90: 'FPCN',
    # 'R inferior parietal lobule; supramarginal gyrus' ->
    # 'Right Supramarginal posterior' (8.2)
    8: 'DN',  # TODO: DN/FPCN!!!
    # 'L ventrolateral prefrontal cortex' -> 'Left Frontal Orbital' (8.3)
    120: 'DN',
    # 'L inferior parietal lobule; angular gyrus' ->
    # 'Left Lateral Occipital superior' (8.8)
    180: 'DN',
    # 'L lingual gyrus' -> 'Left Lingual' (9.7)
    171: 'other',
    # 'Medial prefrontal cortex; anterior cingulate cortex' ->
    # 'Right Paracingulate' (9.7)
    71: 'DN',
    # 'Precuneus; posterior cingulate cortex' -> 'Right Precuneous' (10.1)
    183: 'DN',  # TODO: FPCN/DN!!!
    # 'L temporopolar cortex' -> 'Left Temporal Pole' (11.3)
    38: 'DN',  # TODO: DN/other!!!
    # 'R secondary somatosensory cortex' -> 'Right Superior Parietal Lobule'
    # (12.5)
    82: 'other',
    # 'Rostromedial prefrontal cortex' -> 'Right Paracingulate' (14.3)
    71: 'DN',
}.get(i) for i in range(len(labels))])

secondary_mw_mapping = {
    8: 'FPCN',
    183: 'FPCN',
    38: 'other',
}

mw_distances = {
    3: 4.7,
    123: 6.8,
    88: 7.1,
    90: 8.3,
    8: 8.2,
    120: 8.3,
    180: 8.8,
    171: 9.7,
    71: '9.7; 14.3',
    183: 10.1,
    38: 11.3,
    82: 12.5,
}


null_mapping = numpy.array([None for i in range(len(labels))])


spatial_overlap = {
    # motor
    109: True,  # Right postcentral gyrus
    103: True,  # Left postcentral gyrus

    # goal
    117: True,  # 'Right' anterior cingulate cortex

    # imaginal
    136: True,  # Right Lateral Occipital superior sulcus
    79:  True,  # Left Lateral Occipital superior sulcus

    # retrieval
    41: True,  # Right middle frontal gyrus
    52: True,  # Left middle frontal gyrus
    78: False,  # Right hippocampus
    63: False,  # Left Hippocampus

    # aural
    61:  True,  # Right Superior Temporal posterior gyrus
    28:  False,  # Left Insular
    177: False,  # Left Planum Temporale

    # visual
    77:  True,  # Right Lateral Occipital inferior
    156: False,  # Left Occipital Fusiform
    161: False,  # Right Temporal Occipital Fusiform
    119: False,  # Left Inferior Temporal temporooccipital

    # procedural
    12:  True,  # Right Caudate
    18:  True,  # Left Caudate
    75:  True,  # Left Putamen
    33:  True,  # Right Putamen
    81:  False,  # Right Thalamus
    162: False,  # Left Thalamus
    32:  False,  # Right Thalamus
    19:  False,  # Left Thalamus

    # vocal
    97: False,  # Left Precentral
    42: False,  # Right Postcentral
}


if STATISTICAL_VALIDITY_CHECK:
    # make the mapping random; this means that all statistical tests are
    # comparing a random sample from a population to the remainder of the
    # population. As such, they should not give significant results if they
    # are done correctly.
    numpy.random.seed(1770398048)  # reproducibility
    shuffled_indices = numpy.random.permutation(len(actr_mapping))

    actr_mapping = actr_mapping[shuffled_indices]
    mind_wandering_mapping = mind_wandering_mapping[shuffled_indices]
    new_spatial_keys = numpy.argsort(shuffled_indices)
    spatial_overlap = {new_spatial_keys[key]: value
                       for key, value in spatial_overlap.items()}


with open(os.path.join(path, 'NKI_dti_avg_region_xyz_centers_file.txt')) as f:
    xyz = numpy.array([
        [float(part) for part in line.split()]
        for line in f
    ]).astype(float)
if MERGE_AREAS_WITH_EQUAL_NAME:
    """old [a b c d]:

    [
        [0.0  0.1, 0.2, 0.3],
        [0.4, 0.0, 0.5, 0.6],
        [0.7, 0.8, 0.0, 0.9],
        [1.0, 1.1, 1.2, 0.0],
    ]

    a -> a = 0.0
    a -> b = 0.1
    a -> c = 0.2
    a -> d = 0.3
    b -> a = 0.4
    b -> b = 0.0
    b -> c = 0.5
    b -> d = 0.6
    c -> a = 0.7
    c -> b = 0.8
    c -> c = 0.0
    c -> d = 0.9
    d -> a = 1.0
    d -> b = 1.1
    d -> c = 1.2
    d -> d = 0.0


    new [a(/c) b d]:

    [
        [0.0, 0.9, 1.2],
        [0.9, 0.0, 0.6],
        [2.2, 1.1, 0.0],
    ]

    new(a -> a) = old(a -> a) + old(c -> a) +
                  old(c -> c) + old(a -> c) = 0.9 (but 0.0 by def)
    new(a -> b) = old(a -> b) + old(c -> b) = 0.9
    new(a -> d) = old(a -> d) + old(c -> d) = 1.2

    new(b -> a) = old(b -> a) + old(b -> c) = 0.9
    new(b -> b) = old(b -> b) = 0.0 (also by def)
    new(b -> d) = old(b -> d) = 0.6

    new(d -> a) = old(d -> a) + old(d -> c) = 2.2
    new(d -> b) = old(d -> b) = 1.1
    new(d -> d) = old(d -> d) = 0.0 (also by def)
    """

    multipliers = []
    column = []
    new_indices = {}
    new_labels = []
    new_xyz = []
    new_actr_mapping = []
    new_mw_mapping = []
    indices_generator = itertools.count()
    for label, coordinate, actr_item, mw_item in zip(labels, xyz, actr_mapping,
                                                     mind_wandering_mapping):
        try:
            new_index = new_indices[label]
        except KeyError:
            new_index = next(indices_generator)
            new_indices[label] = new_index
            new_labels.append(label)
            new_xyz.append(coordinate)
            new_actr_mapping.append(actr_item)
            new_mw_mapping.append(mw_item)
            multipliers.append(1)
        else:
            multipliers[new_index] += 1
            new_xyz[new_index] += coordinate
            new_actr_mapping[new_index] = (new_actr_mapping[new_index] or
                                           actr_item)
            new_mw_mapping[new_index] = (new_mw_mapping[new_index] or
                                         mw_item)
        column.append(new_index)

    labels = numpy.array(new_labels)
    actr_mapping = new_actr_mapping
    mind_wandering_mapping = new_mw_mapping

    multipliers = 1 / numpy.array(multipliers, dtype=float)
    old_size = len(column)
    new_size = next(indices_generator)
    mask = numpy.zeros((old_size, new_size))
    if MERGE_AREAS_WITH_EQUAL_NAME == 'mean':
        mask[range(old_size), column] = multipliers[column]
    else:
        mask[range(old_size), column] = 1

    xyz = new_xyz * multipliers[:, numpy.newaxis]


def load_data(id):
    filename = '%s_DTI_connectivity_matrix_file.txt' % id
    connectivity = numpy.loadtxt(os.path.join(path, filename))

    if MERGE_AREAS_WITH_EQUAL_NAME:
        connectivity = connectivity.dot(mask).T.dot(mask).T
        numpy.fill_diagonal(connectivity, 0)

    connectivity /= numpy.max(connectivity)
    return connectivity


def extract_id(filename):
    id = filename.split('_', maxsplit=1)[0]
    if id.isdigit():
        return id


unique_ids = set(extract_id(filename) for filename in os.listdir(path))
ids = sorted(id for id in unique_ids if id is not None)
