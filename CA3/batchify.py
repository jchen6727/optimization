from ca3 import netParams

def get_weight(conn):
    return netParams['connParams'][conn]['weight']

conns = [conn for conn in netParams.connParams.keys() if 'NMDA' in conn] # or 'NMDA' or 'GABA'

weights = [get_weight(conn) for conn in conns]

