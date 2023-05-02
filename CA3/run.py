from avatk.runtk.runners import remote_runner
import pandas
import json


def run(config):
    netm_env = {"NETM{}".format(i):
                    "{}={}".format(key, config[key]) for i, key in enumerate(config.keys())}
    runner = remote_runner(cmdstr = "python runner.py", env = netm_env)
    stdouts, stderr = runner.run()
    print(stdouts)
    data = pandas.Series(json.loads(stdouts.split("DELIM"))[-1])
    return data