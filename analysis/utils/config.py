import os

"""General configuration:"""

# DATA_SET = "hagmann"
DATA_SET = "nkirockland"
# DATA_SET = "finger"
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'out')

STATISTICAL_VALIDITY_CHECK = False
GENERATE_RAW_PLOTS = False
GLOBAL_RANDOM_DISTRIBUTION_SIZE = 100
MULTI_CORE = True

"""General plot configuration"""

PAGE_WIDTH = 6.29921259843  # inches
COLUMN_WIDTH = 3.03149606299  # inches
MODULE_LEVEL_CONDITION = False
SHOW_3D_REPR = False

"""Distribution plot configuration"""

ERROR_BARS = True
PRINT_LABELS = False

"""ACT-R mapping plot"""

STORE_ANIMATION = False

"""NKI Rockland-specific configuration:"""

# DEPRECATED (this is not taken into account by global measure caching):
#
# MERGE_AREAS_WITH_EQUAL_NAME = 'mean'
# MERGE_AREAS_WITH_EQUAL_NAME = 'sum'
MERGE_AREAS_WITH_EQUAL_NAME = False
