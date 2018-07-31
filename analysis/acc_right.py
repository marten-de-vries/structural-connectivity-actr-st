import matplotlib.pyplot as plt
import numpy
import scipy
from .utils.ui import generate_plots
from .utils.plot import mappings_to_colors
from .utils.misc import print_ttest_bayes_factor


def process(data):
    return data[117]  # Right Cingulate anterior


def plot(result, name):
    indices = numpy.argsort(result.labels)
    left = [i for i in indices if result.labels[i].startswith('Left')]
    right = [i for i in indices if result.labels[i].startswith('Right')]
    indices = left + right
    x = range(len(indices))
    colors = mappings_to_colors(*result.mappings)
    plt.figure(0, figsize=(30, 20))
    try:
        yerr = result.stderr[indices]
    except TypeError:
        yerr = None
    plt.bar(x, result.data[indices], color=colors[indices], capsize=3,
            yerr=yerr)
    plt.xticks(x, result.labels[indices], rotation='vertical')
    plt.subplots_adjust(left=0.08, right=0.95, bottom=0.35)

    all_left = numpy.array(result.data[left])
    all_right = numpy.array(result.data[right])

    print('Median(weights to left hemisphere) =', numpy.median(all_left))
    print('Median(weights to right hemisphere) =', numpy.median(all_right))
    print('Mean(weights to left hemisphere) =', numpy.mean(all_left))
    print('Mean(weights to right hemisphere) =', numpy.mean(all_right))

    print('n =', len(all_left) + len(all_right))
    # Cohen's d
    s = numpy.sqrt(
        (
            ((len(all_left) - 1) * numpy.std(all_left, ddof=1)) +
            ((len(all_right) - 1 * numpy.std(all_right, ddof=-1)))
        ) /
        (len(all_left) + len(all_right) - 2)
    )
    d = (numpy.mean(all_right) - numpy.mean(all_left)) / s
    # 'very small'. Combine that with the fact that means make no sense here.
    print("Cohen's d:", d)
    print(scipy.stats.mannwhitneyu(all_left, all_right,
                                   alternative='two-sided'))

    # relatively ok-ish stats
    print_ttest_bayes_factor(all_left, all_right)
    from rpy2 import robjects
    wcox = robjects.r['wilcox.test'](all_left, all_right, **{'conf.int': True})
    # Hodges-Lehmann estimator (better effect size):
    print(wcox.rx('estimate')[0])


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Right ACC connectivity for subject #%s",
                   'accright_%s')
