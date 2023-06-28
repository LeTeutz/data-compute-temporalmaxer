#!/bin/bash
#SBATCH --job-name="train_time"
#SBATCH --partition=gpu
#SBATCH --time=08:00:00
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

for value in {1..5}
do
	echo "start training"
    srun python train_time_compute.py ./configs/temporalmaxer_thumos_i3d.yaml --save_ckpt_dir "./ckpt/thumos" > "train_${value}.txt"

	echo "start testing"
    srun python ./eval.py ./configs/temporalmaxer_thumos_i3d.yaml ./ckpt/thumos/bestmodel.pth.tar > "results_${value}.txt"
done

# Deactivate conda
conda deactivate

