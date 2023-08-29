from netpyne import sim

cfg, netParams = sim.readCmdLineArgs(simConfigDefault='cfg.py', netParamsDefault='netParams.py')

cfg.duration = 100
sim.createSimulateAnalyze(simConfig = cfg, netParams = netParams)

if sim.rank == 0:
    # print output data
    print("===weight===")
    for param in sim.net.params.connParams:
        print("{}: {}".format(param,sim.net.params.connParams[param]['weight']))
    print("===rate===")
    spikes = sim.analysis.popAvgRates(show=False)
    for pop, rate in spikes.items():
        print("{}: {}".format(pop, rate))

