"""
HHTut.py
"""

from netpyne import specs
"""
simConfig
"""
cfg = specs.SimConfig()   # object of class SimConfig to store the simulation configuration

# Simulation parameters
cfg.duration = 1*1e3 # Duration of the simulation, in ms
cfg.dt = 0.025 # Internal integration timestep to use
cfg.seeds = {'conn': 1, 'stim': 1, 'loc': 1} # Seeds for randomizers (connectivity, input stimulation and cell locations)
cfg.verbose = False  # show detailed messages
cfg.hParams = {'v_init': -71}

# Recording
cfg.recordCells = []  # which cells to record from
cfg.recordTraces = {'Vsoma': {'sec': 'soma','loc': 0.5,'var': 'v'}}
cfg.recordStim = True  # record spikes of cell stims
cfg.recordStep = 0.1 # Step size in ms to save data (eg. V traces, LFP, etc)

# Saving
cfg.filename = 'HHTut'  # Set file output name
cfg.saveFileStep = 1000 # step size in ms to save data to disk
cfg.savePickle = False # Whether or not to write spikes etc. to a .mat file
cfg.saveJson = True

# Analysis and plotting
cfg.analysis['plotRaster'] = {'saveData': 'raster_data.json', 'saveFig': True, 'showFig': True} # Plot raster
cfg.analysis['plotTraces'] = {'include': [2], 'saveFig': True, 'showFig': True} # Plot cell traces
cfg.analysis['plot2Dnet'] = {'saveFig': True, 'showFig': True} # Plot 2D cells and connections

"""
netParams
"""
netParams = specs.NetParams()   # object of class NetParams to store the network parameters

# Population parameters
netParams.popParams['PYR'] = {'cellType': 'PYR', 'numCells': 200} # add dict with params for this pop

# Cell parameters
## PYR cell properties
PYRcell = {'secs': {}} # cell rule dict
PYRcell['secs']['soma'] = {'geom': {}, 'mechs': {}} # soma params dict
PYRcell['secs']['soma']['geom'] = {'diam': 18.8, 'L': 18.8, 'Ra': 123.0} # soma geometry
PYRcell['secs']['soma']['mechs']['hh'] = {'gnabar': 0.12, 'gkbar': 0.036, 'gl': 0.003, 'el': -70} # soma hh mechanism
PYRcell['secs']['soma']['vinit'] = cfg.hParams['v_init'] # set initial membrane potential
netParams.cellParams['PYR'] = PYRcell # add dict to list of cell params


# Synaptic mechanism parameters
netParams.synMechParams['AMPA'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 1.0, 'e': 0}


# Stimulation parameters
netParams.stimSourceParams['bkg'] = {'type': 'NetStim', 'rate': 10, 'noise': 0.5, 'start': 1}
netParams.stimTargetParams['bkg->PYR'] = {'source': 'bkg', 'conds': {'pop': 'PYR'}, 'weight': 0.1, 'delay': 'uniform(1,5)'}


# Connectivity parameters
netParams.connParams['PYR->PYR'] = {
    'preConds': {'pop': 'PYR'}, 'postConds': {'pop': 'PYR'},
    'weight': 0.002,                    # weight of each connection
    'delay': '0.2+normal(13.0,1.4)',     # delay min=0.2, mean=13.0, var = 1.4
    'threshold': 10,                    # threshold
    'convergence': 'uniform(1,15)'}    # convergence (num presyn targeting postsyn) is uniformly distributed between 1 and 15
