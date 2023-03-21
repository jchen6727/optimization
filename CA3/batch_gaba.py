"""
example: generate batch with GABA weight parameter sweep
"""

from avatk.runtk.remote_runner import remote_runner
import ray
import numpy
import itertools
import json
import time

@ray.remote
class rr(remote_runner):
    "inherit remote_runner.remote_runner"
    cmdstr = "mpiexec -n 4 nrniv -python -mpi runner.py"

ray.init(num_cpus = 3)

vars = ['BC->BC_GABA' , 'BC->PYR_GABA' , 'OLM->PYR_GABA']
# turn vars into environment variable friendly strings --- change '->' to 'DELIM'
envvars = ['NETM_{}'.format(var.translate({ord(c): 'DELIM' for c in '->'})) for var in vars]
weights = numpy.array([0.0045, 0.00072, 0.072]) # original values of GABA weights
weights = [[ub, lb] for ub, lb in zip(weights * 100, weights / 100)] # create sample space

vwd = { # var: weight dictionary
    v: w for v, w in zip(vars, weights)
}

envstr = ["netParams.connParams.{}.weight".format(var) + " = {}" for var in vars]

runners = []
envs = []

for ixs in itertools.product(range(2), range(2), range(2)):
    env = {
        envvars[i]: envstr[i].format(str(weights[i][ixs[i]])) for i in range(3)
    }
    env["NETM_SAV"] = "cfg.filename = batch/run_{}_{}_{}".format(*ixs)
    envs.append(env)
    runner = rr.remote(env=env)
    runners.append(runner)

tic = time.time()
stdouts  = ray.get([runner.run.remote() for runner in runners])
print("batch simulation run time: {}".format(time.time() - tic))

jsons = []
for stdout, stderr in stdouts:
    jsonstr = stdout.split('DELIM')[-1]
    jsons.append(json.loads(jsonstr))