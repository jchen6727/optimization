from netpyne import sim
from ca3 import netParams, cfg
"""
netParams.connParams['BC->BC_GABA'  ]['weight'] = 0
netParams.connParams['BC->PYR_GABA' ]['weight'] = 0
netParams.connParams['OLM->PYR_GABA']['weight'] = 0
"""
sim.createSimulate(netParams, cfg)