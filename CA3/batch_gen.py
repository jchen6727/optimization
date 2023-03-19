"""
generates batch rather than reading from a CSV.
"""

from avatk.runtk import remote_runner
import ray
import numpy
import itertools
import json
import time

@ray.remote
class my_remote(remote_runner.remote_runner):
    "inherit remote_runner.remote_runner"
    cmdstr = "mpiexec -n 4 nrniv -python -mpi runner.py"
#    def gather_data(self): # file I/O very slow. Using PIPE
#        filename = "{}_data.pkl".format(self.filename)
#        self.data = pickle.load( open(filename, 'rb') )
#        return self.data


ray.init(num_cpus = 3)
# get any of the keys with:
# [conn for conn in netParams.connParams.keys() if r in conn] # r is 'NMDA', 'AMPA', 'GABA'

# vars = ['PYR->BC_AMPA', 'PYR->OLM_AMPA', 'PYR->PYR_AMPA']
# weights = [0.00036, 0.00036, 2e-05]
# vars = ['PYR->BC_NMDA', 'PYR->OLM_NMDA', 'PYR->PYR_NMDA']
# weights = [0.00036, 0.00036, 2e-05]
vars = ['BC->BC_GABA' , 'BC->PYR_GABA' , 'OLM->PYR_GABA']
# turn vars into environment variable friendly strings
envvars = ['NETM_{}'.format(var.translate({ord(c): None for c in '->'})) for var in vars]
weights = numpy.array([0.0045, 0.00072, 0.072]) # see batchify.py
weights = [[ub, lb] for ub, lb in zip(weights * 100, [0, 0, 0])] # create sample space

vwd = { # var: weight dictionary
    v: w for v, w in zip(vars, weights)
}

envstr = [
    "netParams.connParams.{}.weight".format(var) + " = {}" for var in vars
]

runners = []
envs = []

for ixs in itertools.product(range(2), range(2), range(2)):
    env = {
        envvars[i]: envstr[i].format(str(weights[i][ixs[i]])) for i in range(3)
    }
    env["NETM_SAV"] = "cfg.filename = batch/run_{}_{}_{}".format(*ixs)
    envs.append(env)
    runner = my_remote.remote(env=env)
    runners.append(runner)

tic = time.time()
stdouts  = ray.get([runner.run.remote() for runner in runners])
print("batch simulation run time: {}".format(time.time() - tic))

jsons = []
for stdout, stderr in stdouts:
    jsonstr = stdout.split('DELIMDELIMDELIM')[-1]
    jsons.append(json.loads(jsonstr))

#tic = time.time()
#simdatas = ray.get([runner.gather_data.remote() for runner in runners])
#print("batch simulation read time: {}".format(time.time() - tic))

#for simdata in simdatas:
#    print(simdata['net']['params']['connParams']['BC->BC_GABA'])
#    print(simdata['net']['params']['connParams']['BC->PYR_GABA'])
#    print(simdata['net']['params']['connParams']['OLM->PYR_GABA'])
#    print(simdata['simData']['avgRate'])