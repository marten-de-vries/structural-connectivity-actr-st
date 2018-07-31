import bct
from .utils.ui import global_measure


def process(data):
    return bct.efficiency_wei(data, local=False)


if __name__ == '__main__':
    global_measure(process, 'Global efficiency')
