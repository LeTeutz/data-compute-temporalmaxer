import os
import json
import random
import shutil


def contains_all_classes(data_s, all_classes):
    contained_classes = set()
    for video_name, video_data in data_s.items():
        for annotation in video_data['annotations']:
            contained_classes.add(annotation['label'])
    return contained_classes == all_classes


def sample(p, data_train):
    num_videos = round(p * len(data_train))
    videos = [name for name in data_train]
    sampled_videos = random.sample(videos, num_videos)
    data_s = {vid: data_train[vid] for vid in sampled_videos}
    return data_s


def save(out_path, dataset, data_s, data_test, annotations, features_path):
    out_annotations_path = os.path.join(out_path, dataset, 'annotations',
                                        'thumos14.json' if dataset == 'thumos' else 'anet1.3_i3d_filtered.json')
    out_features_path = os.path.join(out_path, dataset, 'i3d_features')

    # Construct annotations
    annotations['database'] = data_s
    for video_name, video_data in data_test.items():
        annotations['database'][video_name] = video_data

    with open(out_annotations_path, 'w') as f:
        f.write(json.dumps(annotations))

    prefix = 'v_' if dataset == 'anet_1.3' else ''
    # Copy features
    for video_name in data_s:
        file_name = prefix + f'{video_name}.npy'
        if "validation" in file_name:
            print(file_name)
        original = os.path.join(features_path, file_name)
        copy = os.path.join(out_features_path, file_name)
        shutil.copy(original, copy)


def main(p, in_path, out_path, dataset, train, test):
    if dataset not in ['thumos', 'anet_1.3']:
        raise ValueError(f'{dataset} is not a valid dataset')

    annotations_path = os.path.join(in_path, dataset, 'annotations',
                                    'thumos14.json' if dataset == 'thumos' else 'anet1.3_i3d_filtered.json')
    features_path = os.path.join(in_path, dataset, 'i3d_features')
    with open(annotations_path, 'r') as f:
        annotations = json.loads(f.read())

    database = annotations['database']

    all_classes = set()
    data_train = {}
    data_test = {}
    for video_name, video_data in database.items():
        for annotation in video_data['annotations']:
            all_classes.add(annotation['label'])

        subset = video_data['subset'].lower()
        if subset == test:
            data_test[video_name] = video_data
        elif subset == train:
            data_train[video_name] = video_data
        else:
            print(f'Unknown split for video {video_name}')

    print(f'Looking for a split for p={p}')
    data_s = sample(p, data_train)
    while not contains_all_classes(data_s, all_classes):
        data_s = sample(p, data_train)
    print(f'Found split for p={p} [{len(data_s)} videos]')

    print('Moving sampled images to a separate folder')
    save(out_path, dataset, data_s, data_test, annotations, features_path)
    print('Finished sampling')


if __name__ == '__main__':
    main(0.1, './data', './experiment', 'thumos', 'validation', 'test')


