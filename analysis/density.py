import bct
from .utils.ui import global_measure


def process(data):
    # single value: density
    density, vertex_count, edge_count = bct.density_und(data)
    return density


if __name__ == '__main__':
    global_measure(process, 'Density')
