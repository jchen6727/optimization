import ray
import subprocess
import os

import itertools

@ray.remote
class rnr(object):
# run net_runner
    def __init__(self, np=1, script="net_runner.py", env={}):
        self.np = np
        self.cmdstr = "mpiexec -n {} nrniv -python -mpi {}".format(np, script).split()
        self.pid = None
        self.env = os.environ.copy()
        self.add_env(env)

    def get_command(self):
        return self.cmdstr

    def add_env(self, env):
        for key in env:
            self.env[key] = env[key]
        return self.env

    def run(self):
        self.proc = subprocess.run(self.cmdstr, env=self.env, text=True, stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE)
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr
        return self.stdout, self.stderr
    
if __name__ == "__main__":
    ray.init()
    vars = ['PYR', 'OLM']
    envstr = {
        'PYR': "netParams.stimSourceParams.IClamp_PYR.amp = {}",
        'OLM': "netParams.stimSourceParams.IClamp_OLM.amp = {}"
    }
    envval = {
        'PYR': [ 25e-3  ,  50e-3,  75e-3  ],
        'OLM': [-12.5e-3, -25e-3, -37.5e-3]
    }
    runners = []
    for i, j in itertools.product(range(3), range(3)):
        env = {
            "NETM_SAV".format(i, j): "cfg.filename = sim_pyr{}_olm{}".format(i, j),
            "NETM_PYR".format(i, j): envstr['PYR'].format(envval['PYR'][i]),
            "NETM_OLM".format(i, j): envstr['OLM'].format(envval['OLM'][i]),
        }
        runner = rnr.remote(np=2, script="net_runner.py", env=env)
        runners.append(runner)
    results = ray.get([runner.run.remote() for runner in runners])
    
    
    
