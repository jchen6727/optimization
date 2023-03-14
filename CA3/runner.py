from avatk.runners import net_runner
from netpyne import sim
from ca3 import netParams, cfg

class my_runner(net_runner.net_runner): #inherit net_runner object, specify sim, netParams and cfg
    sim = sim
    netParams = netParams
    cfg = cfg

if __name__ == "__main__":
    nr = my_runner()
    nr.set_maps()
    nr.create()
    nr.simulate()
    nr.save()