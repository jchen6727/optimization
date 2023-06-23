from avatk.runtk.runners import dispatcher, netpyne_runner
from netpyne import sim

from ca3 import netParams, cfg
import json

SO = '/ddn/jchen/dev/optimization/CA3/mod/x86_64/libnrnmech.so'
MECH = '/ddn/jchen/dev/optimization/CA3/mod'
#DLL = 'mod/x86_64/libnrnmech.so'
#define parameter strings
class nr(netpyne_runner):
    "inherit the process_runner"
    sim = sim
    netParams = netParams
    cfg = cfg

if __name__ == "__main__":
    r = nr()
    r.set_mappings()
    try:
        r.sim.h.hcurrent
    except:
        #neuron.load_mechanisms(MECH)
        r.sim.h.nrn_load_dll(SO)
    #json_out = r.get_mappings()
    #print("DELIM{}".format(json_out))
    r.create()
    r.simulate()
    r.sim.pc.barrier()
    if r.sim.rank == 0: # prepare dictionary to dump to output
        json_out = r.get_mappings()
        data_out = r.sim.analysis.prepareSpikeData()['legendLabels']
        for datm in data_out:
            pop = datm.split('\n')[0]
            freq = datm.split(' ')[-2]
            json_out[pop] = freq
        json_str = json.dumps(json_out)
        print("===FREQUENCIES===\n{}".format(json_str))
        