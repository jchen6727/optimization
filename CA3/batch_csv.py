from avatk.runtk.runners import remote_runner
import ray
import pandas
import json
import numpy

#ray.init(num_cpus=1)
ray.init()

@ray.remote
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

def get_dfs(csv: str, max_nodes: int):
    # reads csv, splits csv into a list of dataframes with size max_nodes
    jobs = pandas.read_csv(csv)
    return [jobs[i:j] for i, j in zip( numpy.arange( 0, len(jobs), max_nodes) , numpy.arange( max_nodes, len(jobs) + max_nodes, max_nodes) )]

def run_df(df: pandas.DataFrame):
    runners = df.apply(init_run, axis=1)
    return runners

def get_data(output: pandas.Series):
    pds = pandas.Series(json.loads(output.split("DELIM")[-1]))
    return pds

def run_csv(in_csv: str, out_csv: str):
    bins = get_dfs(in_csv, 50)
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
    run_csv("batch_csv/run{}.csv".format(i), "batch_csv/out{}.csv".format(i))



"""
def run_csv(csv: str):
    _jobs = pandas.read_csv(csv)
    _runners = _jobs.apply(init_run, axis=1)
    return _jobs, _runners
"""
    
"""
bins = get_dfs("batch_csv/test.csv", 3)
batchdata = []
for _bin in bins:
    runners = run_df(_bin)
    stdouts = runners.apply(get_run)
    batchdata.append(stdouts.apply(get_data))
"""


#jobs, runners = run_csv("batch_csv/test.csv")

# might be better to implement this as a for loop?
#stdouts = runners.apply(get_run)

#del runners