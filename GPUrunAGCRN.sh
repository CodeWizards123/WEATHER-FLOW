#!/bin/sh
#SBATCH --account=a100free
#SBATCH --partition=a100
#SBATCH --nodes=1 --ntasks=4 --gres=gpu:a100-2g-10gb:1
#SBATCH --time=40:00:00
#SBATCH --job-name="AGCRN_gpu"
CUDA_VISIBLE_DEVICES=$(ncvd)
nvcc --version
module load python/miniconda3-py38-usr-A
source activate weatherEnv
python3 runAGCRN.py
