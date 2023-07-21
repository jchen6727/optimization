from pubtk.runtk import NetpyneRunner
#from pubtk.runtk.runners import NetpyneRunner
from netpyne import sim

from ca3 import netParams, cfg
import json

SO = '/ddn/jchen/dev/optimization/CA3/mod/x86_64/libnrnmech.so'
MECH = '/ddn/jchen/dev/optimization/CA3/mod'
#DLL = 'mod/x86_64/libnrnmech.so'
#define parameter strings
class NR(NetpyneRunner):
    "inherit the process_runner"
    sim = sim
    netParams = netParams
    cfg = cfg

    def get_freq(self):
        freq_data = {}
        data = self.sim.analysis.prepareSpikeData()['legendLabels']
        for datm in data:
            pop = datm.split('\n')[0]
            freq = datm.split(' ')[-2]
            freq_data[pop] = freq
        return freq_data

if __name__ == "__main__":
    r = NR()
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
    if r.sim.rank == 0: # data out (print, and then file I/O if writefile specified)
        inputs = r.get_mappings()
        spikes = r.get_freq()
        out_json = json.dumps({**inputs, **spikes})
        print("===FREQUENCIES===\n")
        print(out_json)
        if r.writefile:
            print("")
            r.write(out_json)

