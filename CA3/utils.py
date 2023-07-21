import pandas
import numpy
import json
import os
import time
import hashlib

from pubtk.runtk import Dispatcher, SFS_Dispatcher
from pubtk.runtk.template import sge_template

#from avatk.runtk.runners import dispatcher
#TODO update to asyncio

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
    runner = Dispatcher(cmdstr= cmdstr, env= netm_env)
    stdout, stderr = runner.run()
    data = stdout.split("===FREQUENCIES===\n")[-1]
    runner = Dispatcher(cmdstr= cmdstr, env= netm_env)
    stdout, stderr = runner.run()
    data = stdout.split("===FREQUENCIES===\n")[-1]
    sdata = pandas.Series(json.loads(data)).astype(float)
    return sdata

def sge_run(config, cmdstr, cwd, cores, wait_interval= 5):
    # run on sge
    # create shell script, submit shell script, watch  for output file, return output when complete.
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    dispatcher = SFS_Dispatcher(cmdstr=cmdstr, cwd=cwd, env= netm_env)
    stdouts, stderr = dispatcher.shrun(sh="qsub", 
                                   template=sge_template,
                                   name="ca3",
                                   cores=cores, #NOT THE SAME AS $NSLOTS (which reserves 1 less per SGE)
                                   vmem="32G",
                                   pre="",
                                   post=""
                                   )
    # wait for sig
    # TODO implement asyncio instead
    data = dispatcher.get_shrun()
    while not data:
        time.sleep(wait_interval)
        data = dispatcher.get_shrun()
    #sdata = pandas.Series(json.loads(data)).astype(float)
    dispatcher.clean(args='rw')
    return data, stdouts, stderr

def dbrun(config, cmdstr): 
    # debug optimization run 
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    runner = Dispatcher(cmdstr= cmdstr, env= netm_env)
    stdout, stderr = runner.run()
    return stdout, stderr

def dbobjective(config, cmdstr):
    # debug objective of a remote process
    stdout, stderr = dbrun(config, cmdstr)
    stdout, stderr = dbrun(config, cmdstr)
    loss = 0
    return dict(loss=loss, stdout=stdout, stderr=stderr)

def write_csv(dataframe: pandas.DataFrame, savestring: str):
    if '/' in savestring:
        os.makedirs(savestring.rsplit('/', 1)[0], exist_ok=True)
    dataframe.to_csv(savestring)