"""
use agg_csv from utils to aggregate a list of .csv into one file.

"""
import utils

files = ['batch_NMDA/out{}.csv'.format(i) for i in range(11)]

utils.agg_csv(files, 'NMDAf.csv')

