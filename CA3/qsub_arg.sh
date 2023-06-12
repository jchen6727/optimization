#!/bin/bash

#$ -N optuna
#$ -cwd
#$ -pe smp 30
#$ -l h_vmem=128G

cat qsub_arg.sh
source ~/.bashrc
python optimize.py -c $1 -t $2 -s $3
