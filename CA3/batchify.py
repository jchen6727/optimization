from ca3 import netParams
from avatk.batchtk import batchify

def get_weight(conn):
    return netParams['connParams'][conn]['weight']

conns = [conn for conn in netParams.connParams.keys() if 'AMPA' in conn] # or NMDA or GABA

weights = [get_weight(conn) for conn in conns]

