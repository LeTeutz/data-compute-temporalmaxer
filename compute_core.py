import torch
import torch.nn as nn
import torch.utils.data
import os
import numpy as np
from libs.core import load_config
from libs.modeling import make_meta_arch

def load_model(config_path, checkpoint_path):
    config = load_config(config_path)
    model = make_meta_arch(config["model_name"], **config["model"])
    model = nn.DataParallel(model, device_ids=config["devices"])

    checkpoint = torch.load(checkpoint_path, 
                            map_location=lambda storage, loc: storage.cuda(config["devices"][0]))

    model.load_state_dict(checkpoint["model_state_dict"])
    del checkpoint

    model.eval()
    return model

def construct_sample(feature_length, fps, feature_stride, num_frames, embedding_size=2048, features=None, device='cuda:0'):
    duration = float((feature_length - 1) * feature_stride + num_frames) / fps
    if features is None:
        features = torch.rand((embedding_size, feature_length))
    features.to(device)

    video_list = [{
        'video_id': 'random',
        'feats': features,
        'fps': fps,
        'duration': duration,
        'feat_stride': feature_stride,
        'feat_num_frames': num_frames,
    }]

    return video_list

def run_command(command):
    os.system(f'conda run -n /scratch/toprescu/.conda/envs/tmenv {command}')
