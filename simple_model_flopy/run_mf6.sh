#!/bin/bash
#PBS -l walltime=1:00:00
#PBS -l ncpus=1
#PBS -l mem=1500MB
#PBS -l jobfs=1500MB
#PBS -l wd
#PBS -N modflow6_run

echo "Running in:"
pwd

echo "Using MODFLOW 6 executable:"
which mf6

echo "Running the generated MODFLOW 6 model:"
mf6
