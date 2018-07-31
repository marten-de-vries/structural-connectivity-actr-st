import subprocess
import sys


def run(type, name):
    if 'all' in sys.argv or type in sys.argv or name in sys.argv:
        print("Running (%s): %s" % (type, name))
        subprocess.check_call(['python', '-m', name])


run('local', 'analysis.betweenness')
run('local', 'analysis.degree')
run('local', 'analysis.eigenvector_centrality')
run('local', 'analysis.local_clustering_coefficient')
run('local', 'analysis.local_efficiency')
run('local', 'analysis.pagerank_centrality')
run('local', 'analysis.strength')

run('global', 'analysis.assortativity')
run('global', 'analysis.density')
run('global', 'analysis.global_efficiency')
run('global', 'analysis.transitivity')

run('misc', 'analysis.mapping')
run('misc', 'analysis.legend')
run('misc', 'analysis.tables')
