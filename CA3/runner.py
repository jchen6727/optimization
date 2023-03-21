from avatk.runtk.runners import process_runner, remote_runner
from netpyne import sim
from ca3 import netParams, cfg
import json

#define parameter strings
class pr(process_runner):
    "inherit the process_runner"
    sim = sim
    netParams = netParams
    cfg = cfg

class rr(remote_runner):
    "inherit the remote_runner"
    cmdstr = "mpiexec -n 4 nrniv -python -mpi runner.py"


if __name__ == "__main__":
    r = pr()
    r.set_maps()
    r.create()
    r.simulate()
    r.sim.pc.barrier()
    if r.sim.rank == 0: # prepare dictionary to dump to output
        json_out = r.get_maps()
        data_out = r.sim.analysis.prepareSpikeData()['legendLabels']
        for datm in data_out:
            pop = datm.split('\n')[0]
            freq = datm.split(' ')[-2]
            json_out[pop]  = freq
        json_str = json.dumps(json_out)
        print("DELIM{}".format(json_str))
