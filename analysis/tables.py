import contextlib
import os
# import re

from .utils.config import OUT_DIR
from .utils.misc import open_stats_db
from .data.nkirockland import (actr_mapping, mind_wandering_mapping, xyz,
                               labels, spatial_overlap, mw_distances,
                               secondary_mw_mapping)


def mapping_key(info):
    i, module = info
    # into a sortable format
    label = labels[i].replace('Left', '').replace('Right', '').strip()
    return module if module else '', label, list(xyz[i])


def print_actr_mapping_table():
    # mapping table

    print(r'\small')
    print(r'\begin{tabular}{| l | r @{, } r @{, } r l | l |}\hline')
    print(r'\textbf{ACT--R module} & \multicolumn{4}{c |}'
          r'{\textbf{Brain areas}} & \textbf{Spatial overlap?}\\')
    print(r'& \multicolumn{3}{l}{\textbf{Position}} & '
          r'\textbf{Label} &\\')
    last_mod = None
    MAPPING_ROW = r'{:<10} & {:.1f} & {:.1f} & {:.1f} & {} & {}\\'
    for i, module in sorted(enumerate(actr_mapping), key=mapping_key):
        if module:
            if last_mod == module:
                module = ''  # don't show again
            else:
                print(r'\hline')
                last_mod = module
            coords = xyz[i]
            label = labels[i]
            overlap = r'\checkmark' if spatial_overlap[i] else ''
            print(MAPPING_ROW.format(module, *coords, label, overlap))
    print(r'\hline\end{tabular}')


def print_mw_mapping_table():
    print(r'\small')
    print(r'\begin{tabular}{| l  l | r @{, } r @{, } r l | r |}\hline')
    print(r'\multicolumn{2}{| c |}{\textbf{Network}} & '
          r'\multicolumn{4}{c |}{\textbf{Brain areas}} & '
          r'\textbf{Distance}\\')
    print(r'\textbf{primary} & \textbf{secondary} & '
          r'\multicolumn{3}{l}{\textbf{Position}} & \textbf{Label} &\\')
    last_mod = None
    MAPPING_ROW = r'{:<10} & {:<10} & {:.1f} & {:.1f} & {:.1f} & {} & {}\\'
    for i, module in sorted(enumerate(mind_wandering_mapping), key=mapping_key):
        if module:
            if last_mod != module:
                print(r'\hline')
                last_mod = module
            coords = xyz[i]
            label = labels[i]
            distance = mw_distances[i]
            alt_network = secondary_mw_mapping.get(i, '')
            print(MAPPING_ROW.format(module, alt_network, *coords, label,
                                     distance))
    print(r'\hline\end{tabular}')


def get_key(info):
    name, stats = info
    if stats['type'] == 'global':
        return stats['without_actr_p']
    else:
        bf = stats['actr_ttest_bayes_factor']
        return -max(bf, 1 / bf)


def process_bayes_factor(bf_num):
    if bf_num < 1:
        bf = '1 / ' + fmt(1 / bf_num)
    else:
        bf = fmt(bf_num)
    # Harold Jeffrey's scale
    significance = '*' if bf_num > 10**.5 or (1 / bf_num) > 10**.5 else ' '
    return bf, significance


def db_items(type):
    with open_stats_db() as db:
        for name, stats in sorted(db.items(), key=get_key):
            if stats['type'] != type:
                continue
            yield name, stats


def fmt(num):
    digits = 3
    if num >= 10:
        digits -= 1
    if num >= 100:
        digits -= 1
    if num >= 1000:
        digits -= 1
    return '{:.{}f}'.format(num, digits)


def pm(statistic, variance):
    return '${} \pm {}$'.format(fmt(statistic), fmt(variance))


def print_distribution_table():
    # distribution table

    print(r'\small')
    print(r'\begin{tabular}{| l | r r r | r @{ } l r @{ } l|}\hline')
    print(r'\textbf{Measure} & \multicolumn{3}{c |}{\textbf{Median $\pm$ IQR}} & '
          r'\multicolumn{4}{c |}{$\mathbf{BF_{10}}$} \\')
    print(r'& \textbf{ACT--R} & \textbf{ST} & \textbf{All} & '
          r'\textbf{ACT--R/Else} & & \textbf{ST/Else} & \\\hline')

    ROW_TEMPL = r'{:<30} & {} & {} & {} & {:>8} & {} & {:>8} & {}\\\hline'
    for name, stats in db_items(type='distribution'):
        full_name = {
            'eigenvectorcentrality_mean': 'Eigenvector centrality',
            'pagerankcentrality_mean': 'PageRank centrality',
            'strength_mean': 'Strength',
            'degree_mean': 'Degree',
            'betweenness_mean': 'Node betweenness centrality',
            'localefficiency_mean': 'Local efficiency',
            'localclusteringcoefficient_mean': 'Local clustering coefficient',
        }[name]
        actr_bf_num = stats['actr_ttest_bayes_factor']
        mw_bf_num = stats['mw_ttest_bayes_factor']
        actr_bf, actr_signif = process_bayes_factor(actr_bf_num)
        mw_bf, mw_signif = process_bayes_factor(mw_bf_num)
        # bf = re.sub(r'([0-9]+)e[+]([0-9]+)', r'$\1\cdot 10^{\2}$', bf)

        print(ROW_TEMPL.format(
            full_name,
            pm(stats['actr_median'], stats['actr_iqr']),
            pm(stats['mw_median'], stats['mw_iqr']),
            pm(stats['all_median'], stats['all_iqr']),
            actr_bf, actr_signif, mw_bf, mw_signif
        ))

    print(r'\end{tabular}')


def print_global_table():
    # global table
    print(r'\small')
    print(r'\begin{tabular}{| l | r @{ $\pm$ } r | r @{ $\pm$ } r | r @{ $\pm$ } r | r @{ } l | r @{ } l |}'
          r'\hline')
    print(r'\textbf{Measure} & \multicolumn{6}{c |}{\textbf{mean $\pm$ standard error}} & \textbf{p (ACT--R)} & &'
          r'\textbf{p (ST)} &\\')
    print(r'& \multicolumn{2}{c}{\textbf{ACT--R absent}} & '
          r'\multicolumn{2}{c}{\textbf{ST absent}} & '
          r'\multicolumn{2}{c |}{\textbf{random absent}} & & & &'
          r'\\\hline')

    ROW_TEMPL = (r'{:<17} & {:.3f} & {:.2e} & {:.3f} & {:.2e} & {:.3f} & '
                 r'{:.2e} & {:.3f} & {} & {:.3f} & {}\\\hline')
    for name, stats in db_items(type='global'):
        actr_signif = '*' if stats['without_actr_p'] < 0.05 else ' '
        mw_signif = '*' if stats['without_mw_p'] < 0.05 else ' '
        print(ROW_TEMPL.format(
            name,
            stats['without_actr_mean'], stats['without_actr_stderr'],
            stats['without_mw_mean'], stats['without_mw_stderr'],
            stats['without_random_mean'], stats['without_random_stderr'],
            stats['without_actr_p'], actr_signif,
            stats['without_mw_p'], mw_signif
        ))

    print(r'\end{tabular}')


@contextlib.contextmanager
def table_to_file(filename):
    with open(os.path.join(OUT_DIR, 'tables', filename), 'w') as f:
        with contextlib.redirect_stdout(f):
            yield


def main():
    with table_to_file('mw_mapping.tex'):
        print_mw_mapping_table()
    with table_to_file('actr_mapping.tex'):
        print_actr_mapping_table()
    with table_to_file('distribution.tex'):
        print_distribution_table()
    with table_to_file('global.tex'):
        print_global_table()


if __name__ == '__main__':
    main()
