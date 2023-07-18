import utils
import ray
import pandas
import shutil
import os

import uuid
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
args, call= parser.parse_known_args()
args= dict(args._get_kwargs())

kwargs = {
    'mpiexec': shutil.which('mpiexec'), 'cores': 4, 'nrniv': shutil.which('nrniv'),
    'python': shutil.which('python'), 'script': os.getcwd() + '/runner.py'
}

# singlecore command string
CMDSTR = "{python} {script}".format(**kwargs)

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

def dbobjective(config):
    stdouts, stderr = utils.dbrun(config, CMDSTR)
    loss = 0
    session.report(dict(loss=loss, stdouts=stdouts, stderr=stderr))

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

utils.write_csv(resultsdf, SAVESTR)
