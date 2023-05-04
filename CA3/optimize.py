from avatk.runtk.runners import dispatcher
import ray
import pandas
import json
import numpy

from ray import tune
from ray.air import session
from ray.tune.search.optuna import OptunaSearch


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
    runner = dispatcher(cmdstr = "python runner.py", env = netm_env)
    stdouts, stderr = runner.run()
    print(stdouts)
    data = pandas.Series(json.loads(stdouts.split("DELIM"))[-1])
    return data


def objective(config):
    data = run(config)
    loss = mse(data)
    report = dict(loss=loss, **loss)
    session.report(report)

tuner = tune.Tuner(
    objective,
    tune_config=tune.TuneConfig(
        search_alg=OptunaSearch(),
        num_samples=1,
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