#!/usr/bin/env python3

import sys
import os
import json

def main():
    for filename in sys.argv[1:]:
        process_filename(filename)

def process_filename(filename):
    try:
        with open(filename) as file:
            print(f"Processing {filename}")
            try:
                process_data(json.load(file))
            except json.decoder.JSONDecodeError:
                print(f"Unable to parse content of {filename}")
    except FileNotFoundError:
        print(f"Unable to find {filename}")

def count_labels(data):
    counts = {}
    for element in data:
        name = element['name']
        counts[name] = counts.get(name, 0) + 1
    return counts

def obs_by_labels(data, labels):
    by_label = {}
    for element in data:
        name = element['name']
        if name in labels:
            by_label[name] = by_label.get(name, [])
            by_label[name].append(element)
    return by_label

def file_labels(filename):
    result = []
    with open(filename) as f:
        for line in f.readlines():
            result.append(line.strip())
    return result

def most_common_labels(data, count=20):
    counts = count_labels(data)
    label_freq = sorted(counts.items(), key=lambda x: -x[1])
    return [elem[0] for elem in label_freq][:count]

def obs_score(obs):
    if obs.get('image_id', False):
        return -(obs.get('vote', 0) or 0)
    return 0

def process_data(data):
    # labels = most_common_labels(data)
    labels = file_labels("labels.txt")
    obs_per_label = 100
    train = True
    for obs_list in obs_by_labels(data, labels).values():
        for obs in sorted(obs_list, key=obs_score)[:obs_per_label]:
            download_image(obs, train)
            train = not train

def download_image(obs, train):
    name = obs['name'].replace(' ', '_')
    image_id = obs['image_id']
    path = os.path.join("sample", name)
    if not os.path.exists(path):
        os.makedirs(path)            
    dest = os.path.join(path, f"{image_id}.jpg")
    if image_id:
        cmd = f"curl -o {dest} -L https://mushroomobserver.org/images/thumb/{image_id}.jpg"
        os.system(cmd)
    else:
        print(f"No image id for {dest}")

def count_report(counts):
    label_freq = sorted(counts.items(), key=lambda x: -x[1])
    for name, count in label_freq:
        print(f"{name}: {count}")

main()
