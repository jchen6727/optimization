from avatk.runtk import net_runner
from netpyne import sim
from ca3 import netParams, cfg
import json

#define parameter strings
class my_runner(net_runner.net_runner): #inherit net_runner object, specify sim, netParams and cfg
    sim = sim
    netParams = netParams
    cfg = cfg

if __name__ == "__main__":
    nr = my_runner()
    nr.set_maps()
    nr.create()
    nr.simulate()
    nr.sim.pc.barrier()
    if nr.sim.rank == 0: # prepare dictionary to dump to output
        json_out = nr.get_maps()
        data_out = sim.analysis.prepareSpikeData()['legendLabels']
        for datm in data_out:
            pop = datm.split('\n')[0]
            freq = datm.split(' ')[-2]
            json_out[pop]  = freq
        json_str = json.dumps(json_out)
        print("DELIMDELIMDELIM{}".format(json_str))
