#!/bin/sh
#SBATCH --account=a100free
#SBATCH --partition=a100
#SBATCH --nodes=1 --ntasks=4 --gres=gpu:a100-3g-20gb:1
#SBATCH --time=05:00:00
#SBATCH --job-name="agcrn_gpu"
CUDA_VISIBLE_DEVICES=$(ncvd)
nvcc --version
module load python/miniconda3-py38-usr-A
source activate weatherEnv
python3 runAGCRN.py
