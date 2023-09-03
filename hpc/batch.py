from netpyne.batch import Batch

def slurm(batchCfg):
    template = \
"""#!/bin/bash
#SBATCH --job-name={jobName}
#SBATCH -A csd403
#SBATCH -t 00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=32G
#SBATCH --export=ALL
#SBATCH --partition=shared
#SBATCH -o {jobPath}.run
#SBATCH -e {jobPath}.err
#SBATCH --mail-user=jchen.6727@gmail.com
#SBATCH --mail-type=end

echo "simulating job (ID: $SLURM_JOB_ID)"
time mpirun -n 4 nrniv -python -mpi batchJob.py simConfig={cfgSavePath} netParams={netParamsSavePath}
"""
    return {'submit': 'sbatch {jobPath}.sh'.format(**batchCfg),
            'filename': '{jobPath}.sh'.format(**batchCfg),
            'filescript': template.format(**batchCfg),
            'stderr': -1,
            'stdout': -1}



def runBatch():
    params = {'AMPA': [0.5, 1.0, 1.5]}
    b = Batch(cfgFile='cfg.py', netParamsFile='netParams.py', params=params)
    b.batchLabel = "test"
    b.saveFolder = "data/test"
    b.method = 'grid'

    b.runCfg = {'type': 'custom',
                'function': slurm,
                #'run': False,
                'run': True,
    }
    b.run() # run batch

# Main code
if __name__ == '__main__':
	runBatch()
	# batchNMDA()
