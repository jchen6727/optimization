from avatk.runtk.runners import dispatcher

import pandas
import json
import numpy

from ray import tune
from ray.air import session
from ray.tune.search.optuna import OptunaSearch

TARGET = pandas.Series(
    {'A': 5.0,
     'B': 12.0,
     'C': 21.0}
)

def mse(run: pandas.Series, values = TARGET.keys()):
    freqs = run[values]
    return numpy.square(TARGET - freqs).mean()

def run(config):
    env = {"FLOATPMAP{}".format(i):
           "{}={}".format(key, config[key])for i, key in enumerate(config.keys)}
    dis = dispatcher(cmdstr = "python opt_runner.py", env = env)
    stdouts, stder = dis.run()
