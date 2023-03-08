from netpyne import sim
from netsrc.netParams import netParams
from netsrc.cfg import cfg
import subprocess
import os

"""
def get(self, gs):
    try:
        return self.__getattribute__(gs)
    except:
        return self.__getitem__(gs)
"""

class net_runner(object): # has to run within an mpi by parsing environ 
    def __init__(self):
        self.map_strings = [os.environ[map_string] for map_string in os.environ if 'NETM' in map_string]
        self.netParams = netParams
        self.cfg = cfg
        self.set_maps()

    def __getitem__(self, k):
        try:
            return object.__getattribute__(self, k)
        except:
            raise KeyError(k)

    def set_maps(self):
        for map_string in self.map_strings:
            self.set_map(map_string)

    def set_map(self, map_string):
        # split the map_string based on delimiters
        assign_path, value = map_string.split('=')
        assigns = assign_path.strip().split('.')
        try:
            value = float(value)
        except:
            value = value.strip()
        # crawl assigns array
        crawler = self.__getitem__(assigns[0])
        for gi in assigns[1:-1]:
            crawler = crawler.__getitem__(gi)
        
        crawler.__setitem__(assigns[-1], value)
        return value
    
    def run_sim(self):
        sim.createSimulateAnalyze(self.netParams, self.cfg)

if __name__ == "__main__":
    nr = net_runner()
    nr.set_maps()


"""
bad crawler method -- just inherit netParams or simConfig and define __getitem__ and __setitem__
    if assigns[0] == 'netParams':
    #                 .netParams / cfg             .toplevel
        crawler = self.__getattribute__(assigns[0]).__getattribute__(assigns[1])
        for gi in assigns[2:-1]:
            crawler = crawler.__getitem__(gi)
        crawler.__setitem__(assigns[-1], value)
    if assigns[0] == 'cfg':
        print('cfg')
    return value
"""