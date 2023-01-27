from netpyne import specs
from netpyne.batch import Batch
def batchFunction():
    params = {
        'popParams_PYR_numCells': [200, 300, 400],
        'popParams_BC_numCells' : [ 50,  75, 100],
     }


    b = Batch(cfgFile='src/cfg.py', netParamsFile='src/netParams.py', params=params)

    b.batchLabel = 'batchCA3'
    b.saveFolder = 'output'
    b.method = 'grid'

    b.runCfg = {
        'type': 'mpi_bulletin',
        'script': 'src/init.py',
        'skip': True,
    }

    b.run()

if __name__ == '__main__':
    batchFunction()
