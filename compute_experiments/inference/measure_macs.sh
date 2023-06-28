#!/bin/bash
#SBATCH --job-name="measure_macs"
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

echo ">>>Start measuring macs"
srun python measure_macs.py > "macs.txt"

# Deactivate conda
conda deactivate

