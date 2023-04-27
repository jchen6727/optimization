import pandas
import numpy

TARGET = pandas.Series(
    {'PYR': 2.35,
     'BC': 14.3,
     'OLM': 4.83})

def mse(run: pandas.Series):
    freqs = run[['PYR', 'BC', 'OLM']]
    return numpy.square(TARGET - freqs).mean()
