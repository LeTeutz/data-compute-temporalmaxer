export CUDA_VISIBLE_DEVICES=0
python3 ./train.py ./configs/temporalmaxer_thumos_i3d.yaml --save_ckpt_dir "./ckpt/thumos"
