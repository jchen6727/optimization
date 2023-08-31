from netpyne.batch import Batch

def slurm(batchCfg):
    template = \
"""#!/bin/bash
#SBATCH --job-name={simLabel}
#SBATCH -A csd403
#SBATCH -t 00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=32G
#SBATCH --export=ALL
#SBATCH --partition=shared
#SBATCH -o {jobName}.run
#SBATCH -e {jobName}.err
#SBATCH --mail-user=jchen.6727@gmail.com
#SBATCH --mail-type=end

time mpirun -n 4 nrniv -python -mpi batchJob.py simConfig={cfgSavePath} netParams={netParamsSavePath}
"""
    return {'submit': 'sbatch {jobName}.sh'.format(**batchCfg),
            'filename': '{jobName}.sh'.format(**batchCfg),
            'script': template.format(**batchCfg)}



def runBatch():
    params = {'AMPA': [0.5, 1.0, 1.5]}
    b = Batch(cfgFile='cfg.py', netParamsFile='netParams.py', params=params)
    b.batchLabel = "test"
    b.saveFolder = 'data/'+b.batchLabel
    b.method = 'grid'

    b.runCfg = {'type': 'custom',
                'function': slurm,
                'run': True,
    }
    b.run() # run batch

# Main code
if __name__ == '__main__':
	runBatch()
	# batchNMDA()
