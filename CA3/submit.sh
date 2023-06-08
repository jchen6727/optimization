#!/bin/bash

#$ -N optimization
#$ -cwd
#$ -pe smp 10
#$ -l h_vmem=32G

source ~/.bashrc
python optimize.py
