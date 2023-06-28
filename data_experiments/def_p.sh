#!/bin/bash
#SBATCH --job-name="def_P"
#SBATCH --partition=gpu
#SBATCH --time=04:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --account=Education-EEMCS-Courses-CSE3000

# Load modules:
module load 2022r2
module load cuda/11.6
module load openmpi
module load miniconda3

# Set conda env:
unset CONDA_SHLVL
source "$(conda info --base)/etc/profile.d/conda.sh"

# Activate conda
conda activate /scratch/toprescu/.conda/envs/tmenv

# loop
for value in {1..5}
do

	echo "removing previous videos and annotations"
	rm -r ./experiment/thumos/annotations/*
	rm -r ./experiment/thumos/i3d_features/*

	# replace the p value: 0.1, 0.2, 0.4, 0.6, 0.8, 1.0
	echo "sampling"
	srun python data_efficiency.py > "final_dataset_p0.1_${value}.txt"

	echo "training"
	srun python ./train.py ./configs/temporalmaxer_thumos_i3d.yaml --save_ckpt_dir "./ckpt/thumos"

	# replace the p value: 0.1, 0.2, 0.4, 0.6, 0.8, 1.0
	echo "testing"
	srun python ./eval.py ./configs/temporalmaxer_thumos_i3d.yaml ./ckpt/thumos/bestmodel.pth.tar > "final_accuracy_p0.1_run${value}.txt"

done

# Deactivate conda
conda deactivate
