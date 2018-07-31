import functools
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy

from .config import MODULE_LEVEL_CONDITION
from ..data.nkirockland import (null_mapping, actr_mapping,
                                mind_wandering_mapping)


def module_to_color(module):
    actr = {
        'manual': 'tab:red',
        'goal': 'tab:green',
        'vocal': 'tab:brown',
        'imaginal': 'tab:blue',
        'retrieval': 'tab:pink',
        'procedural': 'tab:olive',
        'aural': 'tab:cyan',
        'visual': 'tab:orange',
    }
    mind_wandering = {
        'FPCN': 'tab:purple',
        'DN': 'goldenrod',
        'other': 'chartreuse',
    }
    if MODULE_LEVEL_CONDITION:
        if module in actr:
            return 'tab:blue'
        elif module in mind_wandering:
            return 'tab:orange'
        else:
            return 'lightgray'
    return actr.get(module) or mind_wandering.get(module, 'tab:gray')


def legend_handles(mapping):
    if MODULE_LEVEL_CONDITION:
        if mapping in ('actr', 'both'):
            yield mpatches.Patch(color='tab:blue',
                                 label='Linked to an ACT--R module')
        if mapping in ('mw', 'both'):
            label = 'Linked to a spontaneous thought network'
            yield mpatches.Patch(color='tab:orange', label=label)
        yield mpatches.Patch(color='lightgray', label='Other')
    else:
        if mapping in ('actr', 'both'):
            yield mpatches.Patch(color='white',
                                 label='Regions linked to the ACT--R')
            yield from (mpatches.Patch(color=module_to_color(mod),
                                       label='%s module' % mod)
                        for mod in ['aural', 'goal', 'imaginal', 'manual',
                                    'procedural', 'retrieval', 'visual',
                                    'vocal'])
        if mapping == 'both':
            yield mpatches.Patch(color='white', label='')
        if mapping in ('mw', 'both'):
            label1 = 'Regions active during spontaneous thought:'
            yield mpatches.Patch(color='white', label=label1)
            yield mpatches.Patch(color=module_to_color('DN'),
                                 label='part of the default network')
            label2 = 'part of the frontoparietal control network'
            yield mpatches.Patch(color=module_to_color('FPCN'), label=label2)
            yield mpatches.Patch(color=module_to_color('other'),
                                 label='other')


def color_legend(mapping, **opts):
    if mapping == 'none':
        return
    plt.legend(handles=list(legend_handles(mapping)), **opts)


def mappings_to_colors(*mappings):
    modules = functools.reduce(numpy.logical_or, mappings)
    return numpy.array([module_to_color(module) for module in modules])


def mappings_for(mapping):
    mappings = [null_mapping]
    if mapping in ('actr', 'both'):
        mappings.append(actr_mapping)
    if mapping in ('mw', 'both'):
        mappings.append(mind_wandering_mapping)
    return mappings


def fix_plot_font():
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('font', size=8)
