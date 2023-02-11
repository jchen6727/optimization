from netpyne import specs

def valid(msg):
    print("\033[92m {}\033[00m".format(msg))

def warning(msg):
    print("\033[93m {}\033[00m".format(msg))


def checkObj(cfg, netParams):
    assert(isinstance(cfg, specs.SimConfig)), "your cfg was not a valid SimConfig object"
    assert(isinstance(netParams, specs.NetParams)), "your netParams was not a valid NetParams object"
    base_cfg_dict = specs.SimConfig().__dict__
    base_ntp_dict = specs.NetParams().__dict__
    for key in cfg.__dict__:
        if key in base_cfg_dict.keys():
            valid("config value {} has been set to {}".format(key, getattr(cfg, key)))
        else:
            warning("config defines value {} which does not exist in the base config".format(key, getattr(cfg, key)))
