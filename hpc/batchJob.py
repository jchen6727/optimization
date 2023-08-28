from netpyne import sim

cfg, netParams = sim.readCmdLineArgs(simConfigDefault='src/cfg.py', netParamsDefault='src/netParams.py')


print(netParams.connParams['PYR->BC_NMDA']['weight'])

sim.createSimulateAnalyze(simConfig = cfg, netParams = netParams)