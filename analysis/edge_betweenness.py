import matplotlib.pyplot as plt
import networkx
from networkx.drawing.nx_agraph import graphviz_layout
import bct

from .utils.plot import mappings_to_colors
from .utils.plot3d import plot_interactive
from .utils.ui import generate_plots
from .utils.misc import memory
from .data.nkirockland import xyz

MIN_EDGE_BETWEENNESS = 17


@memory.cache
def process(data):
    ebc, bc = bct.edge_betweenness_wei(data)
    return ebc


def plot(result, name):
    result.data[result.data < MIN_EDGE_BETWEENNESS] = 0
    graph = networkx.from_numpy_matrix(result.data)
    isolates = set(networkx.isolates(graph))
    graph.remove_nodes_from(isolates)
    widths = [e['weight'] - MIN_EDGE_BETWEENNESS + 1
              for u, v, e in graph.edges(data=True)]

    fig, ax = plot_interactive(mapping='both')
    for (source, target), width in zip(graph.edges(), widths):
        ax.plot(*xyz[[source, target]].T, linewidth=width, c='grey')
    plt.show()

    pos = graphviz_layout(graph)
    colors = [c for i, c in enumerate(mappings_to_colors(*result.mapping))
              if i not in isolates]
    networkx.draw(graph, pos, node_color=colors, width=widths)
    filtered_labels = {i: l for i, l in enumerate(result.labels)
                       if i not in isolates and result.mapping[i]}
    networkx.draw_networkx_labels(graph, pos, filtered_labels)
    plt.axis('equal')


if __name__ == '__main__':
    generate_plots(process, plot,
                   "Edge with edge betweenness ≥ 15 for subject #%s",
                   'edge_betweenness_%s')
