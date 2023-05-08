from avatk.runtk.runners import dispatcher
import ray
import pandas
import json
import numpy

import os
from ray import tune
from ray.air import session
from ray.tune.search.optuna import OptunaSearch

runtime_env = {"working_dir": os.getcwd()}
print(runtime_env)
ray.init(runtime_env=runtime_env)
TARGET = pandas.Series(
    {'PYR': 2.35,
     'BC': 14.3,
     'OLM': 4.83})

class od(dispatcher):
    cmdstr = "python /home/jchen/dev/optimization/CA3/runner.py"

def mse(run: pandas.Series, values = TARGET.keys()):
    freqs = run[values]
    return numpy.square(TARGET - freqs).mean()


def run(config):
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    cmdstr = "python /home/jchen/dev/optimization/CA3/runner.py"
    runner = dispatcher(cmdstr= cmdstr, env= netm_env)
    #stdouts, stderr = os.getcwd(), os.listdir()#runner.run()
    stdouts, stderr = runner.run()
    #data = 5
    #data = pandas.Series(json.loads(stdouts.split("DELIM"))[-1])
    data = stdouts.split("DELIM")[-1]
    return stdouts, stderr, data
"""
#TODO what's wrong with the json.loads of this line?
'{"netParams.connParams.PYR->BC_AMPA.weight": 0.7312057605353772, "netParams.connParams.PYR->OLM_AMPA.weight":
    0.9758342523074881, "netParams.connParams.PYR->PYR_AMPA.weight": 0.6589255901261984,
    "PYR": "42.3", "BC": "40", "OLM": "40"}

    '
"""


def objective(config):
    stdouts, stderr, data = run(config)
    #loss = mse(data)
    loss = 5
    report = dict(stdouts= stdouts, stderr= stderr, data= data, loss=loss)#, **loss)
    session.report(report)




tuner = tune.Tuner(
    objective,
    tune_config=tune.TuneConfig(
        search_alg=OptunaSearch(),
        num_samples=2,
        metric="loss",
        mode="min"
    ),
    param_space={
        "netParams.connParams.PYR->BC_AMPA.weight":  tune.uniform(0, 1),
        "netParams.connParams.PYR->OLM_AMPA.weight": tune.uniform(0, 1),
        "netParams.connParams.PYR->PYR_AMPA.weight": tune.uniform(0, 1),
    }
)

results = tuner.fit()
