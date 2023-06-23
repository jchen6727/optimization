from avatk.runtk.runners import dispatcher

import ray
import pandas
import json
import numpy

import os
import shutil
from ray import tune
from ray.air import session
from ray.tune.search.optuna import OptunaSearch
from ray.tune.search import ConcurrencyLimiter

import argparse

## specify CLI to function
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--concurrency', default=1)
parser.add_argument('-t', '--trials', default=5)
parser.add_argument('-s', '--save', '-o', '--output', default="output/tune")
#parser.add_argument('-python')
args, call= parser.parse_known_args()
args= dict(args._get_kwargs())

kwargs = {
    'mpiexec': shutil.which('mpiexec'),
    'nrniv': shutil.which('nrniv'),
    'cores': 4,
    'python': shutil.which('python'),
    'script': os.getcwd() + '/' + 'runner.py'
}

# singlecore command string
#CMDSTR = "{python} {script}".format(**kwargs)

# multicore command string
CMDSTR = "{mpiexec} -n {cores} {nrniv} -python -mpi -nobanner -nogui {script}".format(**kwargs)
CONCURRENCY = int(args['concurrency'])
NTRIALS = int(args['trials'])
SAVESTR = "{}_{}_{}.csv".format(args['save'], CONCURRENCY, NTRIALS)

ray.init(
    runtime_env={"working_dir": ".", # needed for import statements
                 "excludes": ["*.csv"]}, # limit the files copied
    #_temp_dir=os.getcwd() + '/ray', # keep logs in same folder (keeping resources in same folder as "working_dir")
)

"""
ray.init(
#    num_cpus=CONCURRENCY,
    _temp_dir=os.getcwd() + '/logs',
#    object_store_memory=32e9
#    _system_config={'worker_register_timeout_seconds':60} #TODO doesn't seem to change anything
)
"""

#ray.init(runtime_env={"py_modules": [os.getcwd()]})

TARGET = pandas.Series(
    {'PYR': 2.35,
     'BC': 14.3,
     'OLM': 4.83})

def mse(run: pandas.Series, target: pandas.Series):
    values = target.keys()
    freqs = run[values]
    return numpy.square(target - freqs).mean()


def run(config):
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    cmdstr = CMDSTR
    runner = dispatcher(cmdstr= cmdstr, env= netm_env)
    stdouts, stderr = runner.run()
    data = stdouts.split("===FREQUENCIES===\n")[-1]
    sdata = pandas.Series(json.loads(data)).astype(float)
    return sdata
    
def objective(config):
    sdata = run(config)
    loss = mse(sdata, TARGET)
    report = dict(sdata=sdata, PYR=sdata['PYR'], BC=sdata['BC'], OLM=sdata['OLM'], MSE=loss, loss=loss)#, **loss)
    session.report(report)


def dbrun(config): 
    # debug optimization run 
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    cmdstr = CMDSTR
    runner = dispatcher(cmdstr= cmdstr, env= netm_env)
    stdouts, stderr = runner.run()
    return stdouts, stderr

def dbobjective(config):
    # debug objective of a remote process
    stdouts, stderr = dbrun(config)
    loss = 0
    report = dict(loss=loss, stdouts=stdouts, stderr=stderr)
    session.report(report)

def write_csv(dataframe: pandas.DataFrame, savestring: str):
    if '/' in savestring:
        os.makedirs(savestring.rsplit('/', 1)[0], exist_ok=True)
    dataframe.to_csv(savestring)
    

#algo = tune.with_resources(OptunaSearch(), {'cpu': 4}) #TODO not working, error
algo = ConcurrencyLimiter(searcher=OptunaSearch(), max_concurrent= CONCURRENCY, batch= True)

ampa_space={#AMPA search space
    "netParams.connParams.PYR->BC_AMPA.weight":  tune.uniform(0.36e-4, 0.36e-2),
    "netParams.connParams.PYR->OLM_AMPA.weight": tune.uniform(0.36e-4, 0.36e-2),
    "netParams.connParams.PYR->PYR_AMPA.weight": tune.uniform(0.02e-4, 0.02e-2),
}
gaba_space={#GABA search space
    "netParams.connParams.BC->BC_GABA.weight":   tune.uniform(4.5e-4, 4.5e-2),
    "netParams.connParams.BC->PYR_GABA.weight":  tune.uniform(0.72e-4, 0.72e-2),
    "netParams.connParams.OLM->PYR_GABA.weight": tune.uniform(72e-4, 72e-2),
}
nmda_space={#NMDA search space
    "netParams.connParams.PYR->BC_NMDA.weight":  tune.uniform(1.38e-4, 1.38e-2),
    "netParams.connParams.PYR->OLM_NMDA.weight": tune.uniform(0.7e-4, 0.7e-2),
    "netParams.connParams.PYR->PYR_NMDA.weight": tune.uniform(0.004e-4, 0.004e-2),
}

tuner = tune.Tuner(
    dbobjective,
    tune_config=tune.TuneConfig(
        search_alg=algo,
        num_samples=NTRIALS,
        metric="loss",
        mode="min"
    ),
    param_space=gaba_space
)

results = tuner.fit()

resultsdf = results.get_dataframe()

write_csv(resultsdf, SAVESTR)
