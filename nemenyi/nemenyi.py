from scipy.stats import friedmanchisquare, rankdata, norm
from scipy.special import gammaln
from to_latex import writeTex
import numpy as np
import pandas as pd
import math
import sys
import os

skip_first = False
input_file = sys.argv[1]
output_file = sys.argv[2]
asc = (sys.argv[3] == "ASC")
if(len(sys.argv) > 4):
    skip_first = True

print ("Input: {}".format(input_file))
print ("Output: {}".format(output_file))
print ("ASC? {}".format(asc))
print ("Skip? {}".format(skip_first))

data = pd.read_csv(input_file)
#sys.stdout = open("./temp.property", 'w')

#skip_first = False
#asc  = True

if skip_first:
    data_formated = data.drop(data.columns[0],axis=1)
else:
    data_formated = data

nrow, ncol = data_formated.shape

qAlpha5pct = [1.960, 2.344, 2.569, 2.728, 2.850, 2.948, 3.031, 3.102, 3.164, 3.219, 3.268, 3.313, 3.354, 3.391,
                    3.426, 3.458, 3.489, 3.517, 3.544, 3.569, 3.593, 3.616, 3.637, 3.658, 3.678, 3.696, 3.714, 3.732]
qAlpha10pct = [1.645, 2.052, 2.291, 2.460, 2.589, 2.693, 2.780, 2.855, 2.920, 2.978, 3.030, 3.077, 3.120, 3.159,
                    3.196, 3.230, 3.261, 3.291, 3.319, 3.346, 3.371, 3.394, 3.417, 3.439, 3.459, 3.479, 3.498, 3.516]




dataAsRanks = np.full(data_formated.shape, np.nan)

for i in range(data_formated.shape[0]):
    dataAsRanks[i, :] = rankdata(data_formated.iloc[i,:])
    if asc:
        dataAsRanks[i, :] = len(dataAsRanks[i,:]) - dataAsRanks[i, :] + 1

critDiff = math.sqrt((ncol * (ncol + 1.0)) / (6.0 * nrow))
critDiff_5 = qAlpha5pct[ncol - 2] * critDiff
critDiff_10 = qAlpha10pct[ncol - 2] * critDiff

ranks = np.mean(dataAsRanks, 0)

print ('names=', end='')
print (*data_formated.columns,sep=",")
print ("ranks=",end="")
print (*ranks, sep=",")
print ("cd={}".format(critDiff_5))
print ("width=7")

writeTex(data_formated.columns,ranks,cd=critDiff_5,file_tex=output_file)
#for i in range(ncol):
#    print ("{} = {}".format(data_formated.columns[i],ranks[i]))
#print (data_formated.columns)
#print (ranks)
#print ("Critical Difference (0.05) = {}".format(critDiff_5))
#print ("Critical Difference (0.10) = {}".format(critDiff_10))



#os.remove("temp.property")
