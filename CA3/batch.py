from avatk.runners import remote_runner
import ray
import itertools

@ray.remote
class my_remote(remote_runner.remote_runner):
    "inherit remote_runner.remote_runner"
    cmdstr = "mpiexec -n 3 nrniv -python -mpi runner.py"

