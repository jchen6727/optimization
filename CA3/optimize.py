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

#CMDSTR = "/ddn/jchen/miniconda3/envs/dev/bin/python /ddn/jchen/dev/optimization/CA3/runner.py"
#CMDSTR = "python runner.py"

CORES = 4
kwargs = {
#    'mpiexec': shutil.which('mpiexec'),
#    'cores': CORES,
    'python': shutil.which('python'),
    'script': os.getcwd() + '/' + 'runner.py'
}
#CMDSTR = "{mpiexec} -n {cores} {python} {script}".format(**kwargs)
CMDSTR = "{python} {script}".format(**kwargs)
NTRIALS = 4

ray.init()
TARGET = pandas.Series(
    {'PYR': 2.35,
     'BC': 14.3,
     'OLM': 4.83})

def mse(run: pandas.Series, values = TARGET.keys()):
    freqs = run[values]
    return numpy.square(TARGET - freqs).mean()


def run(config):
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    cmdstr = CMDSTR
    runner = dispatcher(cmdstr= cmdstr, env= netm_env)
    stdouts, stderr = runner.run()
    data = stdouts.split("DELIM")[-1]
    sdata = pandas.Series(json.loads(data)).astype(float)
    return stdouts, stderr, data, sdata
    #return stdouts, stderr

#TODO reduce return values
#TODO place return values in a separate debug version of optimize

def objective(config):
    stdouts, stderr, data, sdata = run(config)
    #stdouts, stderr = run(config)
    loss = mse(sdata)
    #loss = 5
    report = dict(sdata=sdata, PYR=sdata['PYR'], BC=sdata['BC'], OLM=sdata['OLM'], loss=loss)#, **loss)
    #report = dict(loss=loss, stdouts=stdouts, stderr=stderr)
    session.report(report)

algo = ConcurrencyLimiter(searcher=OptunaSearch(), max_concurrent= 2, batch= True)

tuner = tune.Tuner(
    objective,
    tune_config=tune.TuneConfig(
        search_alg=algo,
        num_samples=NTRIALS,
        metric="loss",
        mode="min"
    ),
    param_space={
        "netParams.connParams.PYR->BC_AMPA.weight":  tune.uniform(0.36e-4, 0.36e-2),
        "netParams.connParams.PYR->OLM_AMPA.weight": tune.uniform(0.36e-4, 0.36e-2),
        "netParams.connParams.PYR->PYR_AMPA.weight": tune.uniform(0.02e-4, 0.02e-2),
    }
)

results = tuner.fit()

resultsdf = results.get_dataframe()

resultsdf.to_csv('output/trial.csv')