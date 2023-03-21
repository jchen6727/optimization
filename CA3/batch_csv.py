from avatk.runtk.remote_runner import remote_runner
import ray
import numpy
import itertools
import json
import pandas
import time

#@ray.remote
class rr(remote_runner):
    "inherit remote_runner.remote_runner"
    cmdstr = "mpiexec -n 4 nrniv -python -mpi runner.py"

#ray.init(num_cpus = 1)

batches = []
def get_run(row: pandas.Series):
    env = row.to_dict()
    run = env.pop('run')
    #runner = rr.remote(env=env)
    runner = rr(env=env)
    row['rr'] = runner
    print("created run:\t{}\t with params:\n{}".format(run, env))
    return runner

def to_dict(row: (dict, pandas.Series)):
    row.rename({ key: rename(key) for key in row.axes})
    return row

def rename(name: str):
    name.translate({ord(c): 'DELIM' for c in '->'})
    return name
def run_csv(csv= 'batch_csv/run0.csv'):
    jobs = pandas.read_csv(csv)
    runners = jobs.apply(get_run, axis= 1)
    return jobs, runners

jobs, runners = run_csv()

