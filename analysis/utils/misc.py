import os
import shelve

import joblib
import numpy

from .config import OUT_DIR

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'cache')
memory = joblib.Memory(cachedir=CACHE_DIR, verbose=0)


def print_ttest_bayes_factor(x, y):
    bf = ttest_bayes_factor(x, y)
    msg = 'Bayesian t-test (Rouder et al., 2009):'
    if bf > 1:
        print(msg, 'BF_10 = %s' % bf)
    else:
        print(msg, 'BF_01 = %s' % (1 / bf))


r = {}


def ttest_bayes_factor(x, y, paired=False):
    if not r:
        from rpy2 import robjects
        from rpy2.robjects import numpy2ri
        from rpy2.robjects.packages import importr

        numpy2ri.activate()
        BayesFactor = importr('BayesFactor')
        r['ttestBF'] = BayesFactor.ttestBF
        r['as_vector'] = robjects.r['as.vector']
        r['as_numeric'] = robjects.r['as.numeric']

    result = r['ttestBF'](numpy.array(x), numpy.array(y), paired=paired)
    return r['as_numeric'](r['as_vector'](result))[0]


def open_stats_db():
    return shelve.open(os.path.join(OUT_DIR, 'stats.shelve'), 'c')
