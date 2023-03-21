from avatk.runtk.runners import remote_runner
import ray
import pandas
import time

ray.init(num_cpus=1)


@ray.remote
class rr(remote_runner):
    "inherit remote_runner.remote_runner"
    cmdstr = "mpiexec -n 4 nrniv -python -mpi runner.py"


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
    stdouts = ray.get(rrobj.run.remote())
    return stdouts
def run_csv(csv: str):
    _jobs = pandas.read_csv(csv)
    _runners = _jobs.apply(init_run, axis=1)
    return _jobs, _runners


jobs, runners = run_csv("batch_csv/test.csv")

# might be better to maintain this as a for loop
stdouts = runners.apply(get_run)