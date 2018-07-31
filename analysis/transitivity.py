import bct
from .utils.ui import global_measure


def process(data):
    return bct.transitivity_wu(data)


if __name__ == '__main__':
    global_measure(process, 'Transitivity')
