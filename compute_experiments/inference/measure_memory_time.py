import torch 
import argparse
from compute_utils import load_model, construct_sample, run_command
import time

def memory_test(iteration, length):
    output_file = f'inference_time/memory_{iteration}.txt'
    model = load_model('configs/temporalmaxer_thumos_i3d.yaml', 'ckpt/thumos/bestmodel.pth.tar')
    video_list = construct_sample(length, 30, 4, 16)
    model(video_list)
    torch.cuda.reset_peak_memory_stats()
    model(video_list)
    memory_usage = float(torch.cuda.max_memory_allocated()) / (2**20)
    with open(output_file, 'a') as f:
        f.writelines(f'{length},{memory_usage}\n')

def time_test(iteration, length):
    output_file = f'inference_time/time_{iteration}.txt'
    model = load_model('configs/temporalmaxer_thumos_i3d.yaml', 'ckpt/thumos/bestmodel.pth.tar')
    video_list = construct_sample(length, 30, 4, 16)
    model(video_list)
    start = time.time()
    model(video_list)
    ms = (time.time() - start) * 1000
    with open(output_file, 'a') as f:
        f.writelines(f'{length},{ms}\n')

def main(args):
    video_lengths = list(range(200, 3001, 200))

    for rep in range(5):
        for i, length in enumerate(video_lengths):
            iteration = args.iteration

            print(f'Measuring memory and time for iteration={iteration}, repetition={rep}, video_length={length}')
            print('>>Measuring memory')
            memory_test(iteration, length)
            print('>>Measuring time')
            time_test(iteration, length)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measure memory and time for inference')
    parser.add_argument('--iteration', type=int, default=0, help='Iteration number')
    args = parser.parse_args()
    main(args)