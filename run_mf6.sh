#!/bin/bash
#PBS -l walltime=1:00:00
#PBS -l ncpus=1
#PBS -l mem=1500MB
#PBS -l jobfs=1500MB
#PBS -l wd
#PBS -N modflow6_run

module purge
module load python3

source activate mf6

echo "Running in:"
pwd

echo "Using MODFLOW executable:"
which mf6

mf6
