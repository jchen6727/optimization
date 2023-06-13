import os

def generate_qsub(c, t, o):
    qsub_str = f"""#!/bin/bash
#$



def jobStringHPCSGE(jobName, walltime, vmem, queueName, cores, pre, command, post, log, **kwargs):
    """
    creates string for SUN GRID ENGINE
    https://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html
    recommended optional pre and post commands
    rsync -a $SGE_O_WORKDIR/ $TMPDIR/
    cd $TMPDIR
    <execute command here>
    rsync -a --exclude '*.run' --exclude '*.err' $TMPDIR/ $SGE_O_WORKDIR/
    """
    return f"""#!/bin/bash
#$ -cwd
#$ -N {jobName}
#$ -q {queueName}
#$ -pe smp {cores}
#$ -l h_vmem={vmem}
#$ -l h_rt={walltime}
#$ -o {log}.run
#$ -e {log}.err
{pre}
source ~/.bashrc
{command}
{post}
        """