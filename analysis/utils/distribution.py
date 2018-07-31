import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy
import scipy.stats

from .config import ERROR_BARS, SHOW_3D_REPR, PRINT_LABELS, PAGE_WIDTH
from .misc import ttest_bayes_factor, open_stats_db
from .plot import mappings_to_colors
from .plot3d import plot_interactive


def abbrev(label):
    return (label.replace('Right', 'R')
                 .replace('Left', 'L')
                 .replace('Temporal', 'Temp.')  # TODO: Planum Temporale
                 .replace('Parietal', 'Par.')
                 .replace('Occipital', 'Occ.')
                 .replace('Frontal', 'Fr.')
                 .replace('posterior', 'post.')
                 .replace('anterior', 'ant.')
                 .replace('inferior', 'inf.')
                 .replace('Inferior', 'Inf.')
                 .replace('superior', 'sup.')
                 .replace('Superior', 'Sup.'))


def plot_distribution(result, name):
    if SHOW_3D_REPR:
        plot_interactive(mapping='both',
                         s=[w / max(result.data) * 100 for w in result.data])
        plt.show()

    x_indices = numpy.argsort(result.data)[::-1]
    colors = mappings_to_colors(*result.mappings)[x_indices]
    x = range(len(result.data))

    combined_mapping = numpy.logical_or(*result.mappings)
    relevant_labels = [abbrev(l) if combined_mapping[i] else ''
                       for i, l in enumerate(result.labels)]
    relevant_labels = numpy.array(relevant_labels)[x_indices]

    # * 1.15? No idea why, but it seems to work...
    plt.figure(figsize=(PAGE_WIDTH * 1.15, PAGE_WIDTH / 4))
    ax = plt.subplot(111)
    ax.set_xticks([])
    ax.set_xlabel('Brain region')
    try:
        yerr = result.stderr[x_indices]
    except TypeError:
        yerr = None
    else:
        if PRINT_LABELS:
            print(result.labels[x_indices])
    if not ERROR_BARS:
        yerr = None
    ax.bar(x, result.data[x_indices], color=colors, capsize=0.8, yerr=yerr,
           error_kw={'elinewidth': 0.2, 'capthick': 0.2})
    patches = [
        mpatches.Patch(color=c, label=l)
        for c, l in zip(colors, relevant_labels) if l
    ]
    ax.legend(loc='upper center', bbox_to_anchor=(0.46, -0.15), ncol=3,
              handles=patches, labelspacing=.1, handlelength=1.,
              handleheight=.2, handletextpad=.4, columnspacing=.5)

    # aggregate data: print statistics
    actr = []
    mw = []
    all = []
    not_actr = []
    not_mw = []
    for result_item, actr_item, mw_item in zip(result.data, *result.mappings):
        (actr if actr_item else not_actr).append(result_item)
        (mw if mw_item else not_mw).append(result_item)
        all.append(result_item)

    with open_stats_db() as db:
        db[name] = {
            'type': 'distribution',
            'actr_median': numpy.median(actr),
            'actr_iqr': scipy.stats.iqr(actr),
            'mw_median': numpy.median(mw),
            'mw_iqr': scipy.stats.iqr(mw),
            'all_median': numpy.median(all),
            'all_iqr': scipy.stats.iqr(all),
            'actr_ttest_bayes_factor': ttest_bayes_factor(actr, not_actr),
            'mw_ttest_bayes_factor': ttest_bayes_factor(mw, not_mw),
        }
