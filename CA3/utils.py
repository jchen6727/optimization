import pandas
import numpy

TARGET = pandas.Series(
    {'PYR': 2.35,
     'BC': 14.3,
     'OLM': 4.83})

def mse(run: pandas.Series, values = TARGET.keys()):
    freqs = run[values]
    return numpy.square(TARGET - freqs).mean()

def filter_mse(df: pandas.Dataframe, ub):
    #return df[df.MSE < ub] #cannot use this line with typing
		return df[df['MSE'] < ub]

def agg_csv(files, target=None):
    df = pandas.concat([pandas.read_csv(file) for file in files]).reset_index(drop=True)  
    if target:
        df.to_csv(target, index=False)
    return df  
 
        
    