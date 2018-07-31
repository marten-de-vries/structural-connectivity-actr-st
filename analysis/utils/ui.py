import numpy
import scipy.stats
import matplotlib.pyplot as plt

import inspect
import itertools
import multiprocessing
import os

from .config import (DATA_SET, OUT_DIR, GENERATE_RAW_PLOTS, COLUMN_WIDTH,
                     GLOBAL_RANDOM_DISTRIBUTION_SIZE, MULTI_CORE)
from .plot import fix_plot_font
from .misc import memory, open_stats_db  # , ttest_bayes_factor

if DATA_SET == 'nkirockland':
    from ..data.nkirockland import (load_data, labels, actr_mapping, ids,
                                    mind_wandering_mapping)
elif DATA_SET == 'finger':
    from ..data.finger import (load_data, labels, actr_mapping, ids,
                               mind_wandering_mapping)
else:
    raise ValueError("Unknown data set")


class Result:
    def __init__(self, id, data):
        self.id = id
        self.labels = labels
        self.mappings = [actr_mapping, mind_wandering_mapping]

        self.data = data
        self.stderr = 0  # fallback value


class MeanResult(Result):
    def __init__(self, raw_data):
        try:
            data = numpy.mean(raw_data, axis=0)
            stderr = scipy.stats.sem(raw_data, axis=0)
        except ValueError:  # different dimensions, e.g. rich club
            data = None
            stderr = None
        super().__init__('mean', data)

        self.stderr = stderr
        self.raw_data = raw_data


def generate_plots(process_data, *args):
    raw_data = []
    local_inputs = ((id, None) for id in ids)
    for id, data in calculate_measure(local_inputs, process_data):
        if GENERATE_RAW_PLOTS:
            plot_for_result(Result(id, data[0]), *args)
        raw_data.append(data[0])
    plot_for_result(MeanResult(raw_data), *args)


def plot_for_result(result, generate_plot, title, filename):
    fix_plot_font()
    full_filename = filename % result.id
    generate_plot(result, full_filename)
    if result.id == 'mean':
        path = 'mean'
    else:
        plt.suptitle(title % result.id)
        path = 'raw'
    plt.savefig(os.path.join(OUT_DIR, path, full_filename) + '.pgf',
                bbox_inches='tight')
    plt.clf()


def with_nodes_removed(data, node_indices):
    to_keep_indices = numpy.logical_not(node_indices)
    return data[to_keep_indices, :][:, to_keep_indices]


def global_random_inputs(mapping_idx, iterations):
    numpy.random.seed(3282313181)  # reproducibility
    random_idx = mapping_idx.copy()
    for id in ids:
        for _ in range(iterations):
            numpy.random.shuffle(random_idx)
            yield id, random_idx


def do_calculate(info):
    id, remove_indices = info
    data = load_data(id)
    if remove_indices is not None:
        data = with_nodes_removed(data, remove_indices)
    return id, process_data(data)


def calculate_measure(inputs, current_process_data):
    global process_data
    process_data = current_process_data
    if MULTI_CORE:
        with multiprocessing.Pool() as pool:
            yield from grouped_by_id(pool.imap(do_calculate, inputs))
    else:
        yield from grouped_by_id(do_calculate(input) for input in inputs)


def grouped_by_id(simulations):
    for id, values in itertools.groupby(simulations, key=by_id):
        yield id, [value for _, value in values]


def by_id(data):
    id, result = data
    return id


def process_batches(without_random_raw):
    raw_data = [numpy.mean(values) for _, values in without_random_raw]
    return MeanResult(raw_data)


def diff_distribution(simulations, empirical_values):
    for subj_idx, (_, subj_sims) in enumerate(simulations):
        for value in subj_sims:
            yield value - empirical_values[subj_idx]


def calculate_p(distribution, threshold):
    # two-sided
    distribution = numpy.array(distribution)
    count_a = sum(distribution < threshold)
    count_b = sum(distribution > threshold)
    return 2 * (min(count_a, count_b) + 1) / (len(distribution) + 1)


@memory.cache
def calculate_global(file, process_data, actr_mapping,
                     mind_wandering_mapping, without, iterations=0):
    """The file argument is unused, but there to help the cache distinguish
    between different functions all named 'process'.

    """
    assert file == inspect.getsourcefile(process_data)

    mapping_idx = numpy.array(actr_mapping, dtype=bool)
    mindwandering_idx = numpy.array(mind_wandering_mapping, dtype=bool)

    inputs = {
        'actr': ((id, mapping_idx) for id in ids),
        'mindwandering': ((id, mindwandering_idx) for id in ids),
        'random': global_random_inputs(mapping_idx, iterations),
        'random_mw': global_random_inputs(mindwandering_idx, iterations),
    }[without]
    raw = list(calculate_measure(inputs, process_data))
    mean_result = process_batches(raw)
    return raw, mean_result


def global_measure(process_data, name):
    func_args = (inspect.getsourcefile(process_data), process_data,
                 actr_mapping, mind_wandering_mapping)
    _, without_actr = calculate_global(*func_args, 'actr')
    _, without_mw = calculate_global(*func_args, 'mindwandering')
    result = calculate_global(*func_args, 'random',
                              GLOBAL_RANDOM_DISTRIBUTION_SIZE)
    without_random_raw, without_random = result
    result2 = calculate_global(*func_args, 'random_mw',
                               GLOBAL_RANDOM_DISTRIBUTION_SIZE)
    without_random_mw_raw, without_random_mw = result2

    diffs = list(diff_distribution(without_random_raw, without_actr.raw_data))
    # plt.subplot(121)
    # plt.hist(diffs, bins=50)
    # print('diff distribution based (actr): p =', calculate_p(diffs, 0))
    mw_diffs = list(diff_distribution(without_random_mw_raw,
                                      without_mw.raw_data))
    # plt.subplot(122)
    # plt.hist(mw_diffs, bins=50)
    # print('diff distribution based (mw): p =', calculate_p(mw_diffs, 0))
    # plt.show()
    # plt.clf()

    fix_plot_font()
    plt.figure(0, figsize=(COLUMN_WIDTH, COLUMN_WIDTH * 2 / 3))
    plt.violinplot([without_random.raw_data, without_actr.raw_data,
                    without_mw.raw_data], showmeans=True)
    plt.xticks([1, 2, 3], ['without\nrandom\nregions',
                           'without\nACT--R\nregions',
                           'without\nST\nregions'])
    plt.xlabel('measure values')
    plt.ylabel(name.lower())
    plt.savefig(os.path.join(OUT_DIR, name.lower().replace(' ', '_') + '.pgf'),
                bbox_inches='tight')
    plt.clf()

    with open_stats_db() as db:
        db[name] = {
            'type': 'global',
            'without_actr_mean': without_actr.data,
            'without_actr_stderr': without_actr.stderr,
            'without_mw_mean': without_mw.data,
            'without_mw_stderr': without_mw.stderr,
            'without_random_mean': without_random.data,
            'without_random_stderr': without_random.stderr,
            'without_actr_p': calculate_p(diffs, 0),
            'without_mw_p': calculate_p(mw_diffs, 0),
        }
