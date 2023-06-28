#!/bin/bash
#SBATCH --job-name="mem_time"
#SBATCH --partition=gpu
#SBATCH --time=05:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --account=Education-EEMCS-Courses-CSE3000

module load 2022r2
module load cuda/11.6
module load openmpi
module load miniconda3

# Set conda env:
unset CONDA_SHLVL
source "$(conda info --base)/etc/profile.d/conda.sh"

# Activate conda
conda activate /scratch/toprescu/.conda/envs/tmenv

echo ">>>Start measuring memory and time"
srun python measure_memory_time.py --iteration=$1 > "memory_time.txt" 

# Deactivate conda
conda deactivate

