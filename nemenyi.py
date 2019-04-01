import argparse
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy.special import gammaln
from scipy.stats import friedmanchisquare, norm, rankdata

from utils.to_latex import writeTex


parser = argparse.ArgumentParser(description='Creates a critical distance diagram '
                                 'using the Friedman statistical test and the '
                                 'post-hoc Nemenyi analysis.')
parser.add_argument('input', type=str,
                    help='input file containing the performance metrics of each algorithm')
parser.add_argument('output', type=str, help='.tex file')
parser.add_argument('--h', default=False,
                    help='higher values are better', action='store_true')
parser.add_argument('--l', default=False,
                    help='lower values are better', action='store_true')
parser.add_argument('--ignore_first_column', default=False,
                    help='ignores first column', action='store_true')
args = parser.parse_args()

input_file = args.input
output_file = args.output
lower_is_better = args.l
higher_is_better = args.h

assert (lower_is_better is True and higher_is_better is False) or \
    (lower_is_better is False and higher_is_better is True)

ignore_first_column = args.ignore_first_column

print("input file: {}".format(input_file))
print("output file: {}".format(output_file))
print("higher_is_better? {}".format(higher_is_better))
print("ignore first column? {}".format(ignore_first_column))

data = pd.read_csv(input_file)
if ignore_first_column:
    data = data.iloc[:, 1:]

columns = data.columns
data = data.values

qAlpha5pct = [1.960, 2.344, 2.569, 2.728, 2.850, 2.948, 3.031, 3.102, 3.164, 3.219, 3.268, 3.313, 3.354, 3.391,
              3.426, 3.458, 3.489, 3.517, 3.544, 3.569, 3.593, 3.616, 3.637, 3.658, 3.678, 3.696, 3.714, 3.732]

qAlpha10pct = [1.645, 2.052, 2.291, 2.460, 2.589, 2.693, 2.780, 2.855, 2.920, 2.978, 3.030, 3.077, 3.120, 3.159,
               3.196, 3.230, 3.261, 3.291, 3.319, 3.346, 3.371, 3.394, 3.417, 3.439, 3.459, 3.479, 3.498, 3.516]


dataAsRanks = np.full(data.shape, np.nan)
for i, row in enumerate(data):
    dataAsRanks[i, :] = rankdata(row)
    if higher_is_better:
        dataAsRanks[i, :] = len(dataAsRanks[i, :]) - dataAsRanks[i, :] + 1

nrow, ncol = data.shape
critDiff = math.sqrt((ncol * (ncol + 1.0)) / (6.0 * nrow))
critDiff_5 = qAlpha5pct[ncol - 2] * critDiff
critDiff_10 = qAlpha10pct[ncol - 2] * critDiff

ranks = np.mean(dataAsRanks, 0)

caption = f'Nemenyi - {os.path.basename(input_file)}'
writeTex(columns, ranks, critDiff_5, output_file, caption=caption)
