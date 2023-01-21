from netpyne import specs
from netpyne.batch import Batch
def batchFunction():
    params = specs.ODict()
    
    b = Batch(cfgFile='src/cfg.py', netParamsFile='src/netParams.py', params=params)
