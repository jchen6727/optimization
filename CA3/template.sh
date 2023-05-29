#!/bin/bash

#$ -N <jobname>
#$ -cwd
#$ -pe smp <corecount>
#$ -l h_vmem=<memoryvalue>G

cd $TMPDIR
mkdir input
rsync -av $SGE_O_WORKDIR/references/ input/
mkdir results
PROGRAM --inFiles $TMPDIR/input --outFiles $TMPDIR/results --parallel $NSLOTS
rsync -av $TMPDIR/results/ $SGE_O_WORKDIR/processed/
