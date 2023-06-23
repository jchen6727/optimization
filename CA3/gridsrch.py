import utils
import ray
import pandas
import shutil
import os

import numpy
from ray import tune
from ray.air import session
from ray.tune.search.optuna import OptunaSearch
from ray.tune.search import ConcurrencyLimiter

import argparse

## specify CLI to function
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--concurrency', default=1)
parser.add_argument('-d', '-div', nargs=3, type=float, default=[0.5, 1.5, 3])
parser.add_argument('-s', '--save', '-o', '--output', default="output/grid")
parser.add_argument('-p', '--params', nargs='+', default=['PYR->BC_AMPA', 'PYR->OLM_AMPA', 'PYR->PYR_AMPA'])

args, call= parser.parse_known_args()
args= dict(args._get_kwargs())

kwargs = {
    'mpiexec': shutil.which('mpiexec'), 'cores': 4, 'nrniv': shutil.which('nrniv'),
    'python': shutil.which('python'), 'script': os.getcwd() + '/runner.py'
}

# singlecore command string
#CMDSTR = "{python} {script}".format(**kwargs)

# multicore command string
CMDSTR = "{mpiexec} -n {cores} {nrniv} -python -mpi -nobanner -nogui {script}".format(**kwargs)
CONCURRENCY = int(args['concurrency'])
NTRIALS = int(args['trials'])
SAVESTR = "{}_{}.csv".format(args['save'], CONCURRENCY, NTRIALS)

ray.init(runtime_env={"working_dir": "."}) # needed for import statements
#ray.init(runtime_env={"py_modules": [os.getcwd()]})
TARGET = pandas.Series(
    {'PYR': 2.35,
     'BC': 14.3,
     'OLM': 4.83})

def objective(config):
    sdata = utils.run(config, CMDSTR)
    loss = utils.mse(sdata, TARGET)
    report = dict(sdata=sdata, PYR=sdata['PYR'], BC=sdata['BC'], OLM=sdata['OLM'], loss=loss)
    session.report(report)

algo = ConcurrencyLimiter(searcher=OptunaSearch(), max_concurrent= CONCURRENCY, batch= True)

initial_params = { # weights from cfg, AMPA, GABA, NMDA
    'PYR->BC_AMPA' : 0.36e-3, "BC->BC_GABA"  : 4.5e-3 , "PYR->BC_NMDA" : 1.38e-3 ,
    'PYR->OLM_AMPA': 0.36e-3, "BC->PYR_GABA" : 0.72e-3, "PYR->OLM_NMDA": 0.7e-3  ,
    'PYR->PYR_AMPA': 0.02e-3, "OLM->PYR_GABA": 72e-3  , "PYR->PYR_NMDA": 0.004e-3,
}

param_space = { # create parameter space
    "netParams.connParams.{}.weight".format(k): numpy.linspace(v*args['div'][0], v*args['div'][1], int(args['div'][2])) 
    for k, v in initial_params.items() if k in args['params']
}

print("=====grid search=====")
print(param_space)

tuner = tune.Tuner(
    objective,
    tune_config=tune.TuneConfig(
        search_alg=algo,
        num_samples=1, # grid search samples 1 for each param
        metric="loss"
    ),
    param_space=param_space,
)

results = tuner.fit()

resultsdf = results.get_dataframe()

utils.write_csv(resultsdf, SAVESTR)
