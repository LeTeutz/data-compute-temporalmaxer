from compute_core import load_model, construct_sample
from fvcore.nn import FlopCountAnalysis
import torch

def main():
    tensor_lengths = list(range(200, 3001, 200))
    for length in tensor_lengths:
        model = load_model('configs/temporalmaxer_thumos_i3d.yaml', 'ckpt/thumos/bestmodel.pth.tar')
        video_list = construct_sample(length, 30, 4, 16)
        macs = FlopCountAnalysis(model, video_list)
        gmacs = macs.total() / 1e9
        print(f'Length: {length}, GMACs: {gmacs}')

if __name__ == '__main__':
    main()