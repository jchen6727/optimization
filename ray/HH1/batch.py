from avatk.runners import remote_runner
import ray
import itertools


@ray.remote
class my_remote(remote_runner.remote_runner):
    "inherit remote_runner.remote_runner"

ray.init()
vars = ['PYR', 'OLM']
envstr = {
    'RATE'  : "netParams.stimSourceParams.bkg.rate = {}",
    'WEIGHT': "netParams.stimTargetParams.bkg->PYR.weight = {}"
}
envval = {
    'RATE'  : [ 5   , 10 , 15  ],
    'WEIGHT': [ 0.05, 0.1, 0.15]
}
runners = []
envs = []
for i, j in itertools.product(range(3), range(3)):
    env = {
        "NETM_SAV"   : "cfg.filename = batch/RATE_{}_WEIGHT_{}".format(i, j),
        "NETM_RATE"  : envstr['RATE'  ].format(envval['RATE'  ][i]),
        "NETM_WEIGHT": envstr['WEIGHT'].format(envval['WEIGHT'][j]),
    }
    envs.append(env)
    runner = my_remote.remote(np=2, script="runner.py", env=env)
    runners.append(runner)
stdouts  = ray.get([runner.run.remote() for runner in runners])
simdatas = ray.get([runner.gather_data.remote() for runner in runners])
for simdata in simdatas:
    print(simdata['net']['params']['stimSourceParams'])
    print(simdata['net']['params']['stimTargetParams'])
    print(simdata['simData']['avgRate'])