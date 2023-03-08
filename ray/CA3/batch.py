import ray
import subprocess
import os

@ray.remote
class rnr(object):
# run net_runner
    def __init__(self, np=1, script="net_runner.py"):
        self.np = np
        self.cmdstr = "mpiexec -n {} nrniv -python -mpi {}".format(np, script).split()
        self.pid = None
        self.env = os.environ.copy()

    def get_command(self):
        return self.cmdstr

    def add_env(self, envars):
        for var in envars:
            self.env[var] = envars[var]
        return self.env

    def run(self):
        self.proc = subprocess.run(self.cmdstr, env=self.env, text=True, stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE)
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr
        return self.stdout, self.stderr
    
if __name__ == "__main__":
    ray.init()
    envars = [
        'netParams.stimSourceParams.IClamp_PYR.amp = '
        'netParams.stimSourceParams.IClamp_OLM.amp = '
    ]
    pyr_amps = [ 25e-3  ,  50e-3,  75e-3  ]
    olm_amps = [-12.5e-3, -25e-3, -37.5e-3]
netParams.stimSourceParams['IClamp_PYR'] =  {'type': 'IClamp', 'del': 2*0.1, 'dur': 1e9, 'amp': 50e-3}
netParams.stimSourceParams['IClamp_OLM'] =  {'type': 'IClamp', 'del': 2*0.1, 'dur': 1e9, 'amp': -25e-3}