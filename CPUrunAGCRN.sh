#!/bin/sh
#SBATCH --account compsci
#SBATCH --partition=ada
#SBATCH --time=40:00:00
#SBATCH --nodes=1 --ntasks=24
#SBATCH --job-name="CPUagcrn"
#SBATCH --mail-user=gbxade002@uct.ac.za
#SBATCH --mail-type=ALL
module load python/miniconda3-py38-usr-A
source activate weatherEnv
python3 runAGCRN.py
