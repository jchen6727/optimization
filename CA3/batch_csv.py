from avatk.runtk.runners import remote_runner
import ray
import pandas
import json
import numpy

import argparse
import time


#ray.init(num_cpus=1)
ray.init()

@ray.remote(num_cpus= 4)
class rr(remote_runner):
    "inherit remote_runner.remote_runner"
#    cmdstr = "mpiexec -n 4 nrniv -python -mpi runner.py"
    cmdstr = "python runner.py"

def init_run(row: pandas.Series):
    env = row.to_dict()
    run = env.pop('run')
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, env[key]) for i, key in enumerate(env.keys())}
    # runner = rr.remote(env=netm_env)
    runner = rr.remote(env=netm_env)
    print("created run:\t{}\t with environment:\n{}".format(run, netm_env))
    return runner

def get_run(rrobj: remote_runner):
    stdouts, stderr = ray.get(rrobj.run.remote())
    if not stderr:
        print(stderr)
    return stdouts

def get_dfs(csv: str, concurrency: int):
    # reads csv, splits csv into a list of dataframes with size concurrency
    jobs = pandas.read_csv(csv)
    return [jobs[i:j] for i, j in zip( numpy.arange( 0, len(jobs), concurrency) , numpy.arange( concurrency, len(jobs) + concurrency, concurrency) )]

def run_df(df: pandas.DataFrame):
    runners = df.apply(init_run, axis=1)
    return runners

def get_data(output: pandas.Series):
    pds = pandas.Series(json.loads(output.split("DELIM")[-1]))
    return pds

def run_csv(in_csv: str, out_csv: str, concurrency: int):
    bins = get_dfs(in_csv, concurrency)
    print("read: {}".format(in_csv))
    outlist = []
    for _bin in bins:
        runners = run_df(_bin)
        stdouts = runners.apply(get_run)
        df = stdouts.apply(get_data)
        print(df)
        outlist.append(df)
    outdf = pandas.concat(outlist)
    outdf.to_csv(out_csv)
    print("wrote: {}".format(out_csv))
    return outdf

for i in range(11):
    run_csv("batch_csv/run{}.csv".format(i), "batch_csv/out{}.csv".format(i), 3)
