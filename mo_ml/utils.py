#!/usr/bin/env python3

import sys
import os
import json

def download(taxa, obs_per_taxon, json_filename, image_dir="sample"):
    try:
        with open(json_filename) as file:
            try:
                _process_data(json.load(file), taxa, obs_per_taxon, image_dir)
            except json.decoder.JSONDecodeError:
                print(f"Unable to parse content of {filename}")
    except FileNotFoundError:
        print(f"Unable to find {filename}")

def _process_data(data, labels, obs_per_label, image_dir):
    for obs_list in _obs_by_labels(data, labels).values():
        for obs in sorted(obs_list, key=_obs_score)[:obs_per_label]:
            _download_image(obs, image_dir)

def _obs_by_labels(data, labels):
    by_label = {}
    for element in data:
        name = element['name']
        if name in labels:
            by_label[name] = by_label.get(name, [])
            by_label[name].append(element)
    return by_label

def _obs_score(obs):
    if obs.get('image_id', False):
        return -(obs.get('vote', 0) or 0)
    return 0

def _download_image(obs, image_dir):
    name = obs['name'].replace(' ', '_')
    image_id = obs['image_id']
    path = os.path.join(image_dir, name)
    if not os.path.exists(path):
        os.makedirs(path)            
    dest = os.path.join(path, f"{image_id}.jpg")
    if image_id:
        cmd = f"curl -o {dest} -L https://mushroomobserver.org/images/thumb/{image_id}.jpg"
        os.system(cmd)
    else:
        print(f"No image id for {dest}")

def file_labels(filename):
    result = []
    with open(filename) as f:
        for line in f.readlines():
            result.append(line.strip())
    return result

def most_common_labels(data, count=20):
    counts = _count_labels(data)
    label_freq = sorted(counts.items(), key=lambda x: -x[1])
    return [elem[0] for elem in label_freq][:count]

def _count_labels(data):
    counts = {}
    for element in data:
        name = element['name']
        counts[name] = counts.get(name, 0) + 1
    return counts

# def count_report(counts):
#     label_freq = sorted(counts.items(), key=lambda x: -x[1])
#     for name, count in label_freq:
#         print(f"{name}: {count}")

def main():
    for filename in sys.argv[1:]:
        download(file_labels("labels.txt"), 100, filename)

if (__name__ == '__main__'):
    main()
