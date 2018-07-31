import matplotlib.pyplot as plt

import os

from .utils.config import OUT_DIR, COLUMN_WIDTH
from .utils.plot import fix_plot_font, color_legend

if __name__ == '__main__':
    fix_plot_font()
    # Make as small as possible while fitting in the column
    plt.figure(figsize=(COLUMN_WIDTH, COLUMN_WIDTH / 2.1))
    plt.axis('off')
    color_legend(mapping='both', loc='center', frameon=False)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, 'legend.pgf'),
                bbox_inches='tight')
