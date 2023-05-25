#!/bin/bash

#$ -N optimization
#$ -cwd
#$ -pe smp 10
#$ -l h_vmem=32G

#cd $TMPDIR

#echo $SGE_O_WORKDIR

cd $TMPDIR
mkdir input
mkdir output

rsync -a $SGE_O_WORKDIR/ $TMPDIR/input/

# see the submission script
cat $SGE_O_WORKDIR/submit.sh

cd input
#mkdir input
#rsync -av $SGE_O_WORKDIR/references/ input/
tree
#conda activate dev
~/miniconda3/envs/dev/bin/python optimize.py --inFiles $TMPDIR/input --outFiles $TMPDIR/output --parallel $NSLOTS
rsync -a $TMPDIR/output $SGE_O_WORKDIR/processed/
