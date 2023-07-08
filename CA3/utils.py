import pandas
import numpy
import json
import os

from pubtk.runtk.runners import dispatcher
#from avatk.runtk.runners import dispatcher

target = pandas.Series(
    {'PYR': 2.35,
     'BC': 14.3,
     'OLM': 4.83})

def mse(run: pandas.Series, target: pandas.Series):
    values = target.keys()
    freqs = run[values]
    return numpy.square(target - freqs).mean()

def filter_mse(df: pandas.DataFrame, ub):
    return df[df['MSE'] < ub] # return df[df.MSE < ub] #cannot use this line with typing


def agg_csv(files, target=None):
    df = pandas.concat([pandas.read_csv(file) for file in files]).reset_index(drop=True)  
    if target:
        df.to_csv(target, index=False)
    return df

def run(config, cmdstr):
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    runner = dispatcher(cmdstr= cmdstr, env= netm_env)
    stdouts, stderr = runner.run()
    data = stdouts.split("===FREQUENCIES===\n")[-1]
    sdata = pandas.Series(json.loads(data)).astype(float)
    return sdata

def sge_run(config, cmdstr, wait_interval= None):
    # run on sge
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    runner = dispatcher(cmdstr= cmdstr, env= netm_env)
    stdouts, stderr = runner.run()
    data = stdouts.split("===FREQUENCIES===\n")[-1]
    sdata = pandas.Series(json.loads(data)).astype(float)
    return sdata

def dbrun(config, cmdstr): 
    # debug optimization run 
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    runner = dispatcher(cmdstr= cmdstr, env= netm_env)
    stdouts, stderr = runner.run()
    return stdouts, stderr

def dbobjective(config, cmdstr):
    # debug objective of a remote process
    stdouts, stderr = dbrun(config, cmdstr)
    loss = 0
    return dict(loss=loss, stdouts=stdouts, stderr=stderr)


def write_csv(dataframe: pandas.DataFrame, savestring: str):
    if '/' in savestring:
        os.makedirs(savestring.rsplit('/', 1)[0], exist_ok=True)
    dataframe.to_csv(savestring)