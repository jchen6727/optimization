#!/bin/bash
#SBATCH --job-name=mpi_test
#SBATCH -A csd403
#SBATCH -t 00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=32G
#SBATCH --export=ALL
#SBATCH --partition=shared
#SBATCH -o mpi_test.run
#SBATCH -e mpi_test.err
#SBATCH --mail-user=jchen.6727@gmail.com
#SBATCH --mail-type=end

time mpirun -n 4 nrniv -python -mpi init.py
