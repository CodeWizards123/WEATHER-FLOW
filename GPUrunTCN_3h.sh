#!/bin/sh
#SBATCH --account=a100free
#SBATCH --partition=a100
#SBATCH --nodes=1 --ntasks=8 --gres=gpu:a100-2g-10gb:1
#SBATCH --time=25:00:00
#SBATCH --job-name="tcn_gpu_3h"
CUDA_VISIBLE_DEVICES=$(ncvd)
#SBATCH --mail-user=gbxade002@myuct.ac.za
#SBATCH --mail-type=BEGIN,END,FAIL
nvcc --version
module load python/miniconda3-py38-usr-A
source activate weatherEnv
python3 runTCN_3h.py
