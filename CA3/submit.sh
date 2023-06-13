#!/bin/bash

#$ -N optimization
#$ -cwd
#$ -pe smp 10
#$ -l h_vmem=128G

source ~/.bashrc
python optimize.py -c 10 -t 500 -s output/trial
