# Build archive of 100 taxa with 100 images
# mo.json, images_observations.csv
# 100 most common species names
# 100 images, select first image from each reasonable obs (vote_cache > 1.5)
# then fill in with additional passes

import sys
import json
import csv
import argparse

class MoArchive:
    EXCLUSION_LIST = ['Mixed collection']

    def __init__(self, args):
        self.args = args
        with open(args.obs_json) as json_file:
            self.obs_json = json.load(json_file)
        self.bad_images = _bad_images(args.images_csv)
        self.obs_to_images = _obs_to_images(args.images_obs_csv, self.bad_images)
        self.selected_images = {} # label => Set of images_ids

    def build(self):
        labels = self.find_labels()
        obs_lists = self.obs_by_labels(labels).values()
        images_found = 1
        count = 0
        while images_found > 0:
            images_found = self.images_pass(obs_lists)
            count += images_found
        self.print_script()

    def find_labels(self):
        labels = _file_labels(self.args.label_file)
        taxon_count = self.args.taxa
        if taxon_count > len(labels):
            labels += self.most_common_labels(taxon_count - len(labels))
        return labels

    def print_script(self):
        print("dest=sample\nmkdir $dest\nsrc=thumb\n\n")
        for label, image_ids in self.selected_images.items():
            dirname = label.replace(' ', '_')
            print(f"# {label}: {len(image_ids)}")
            print(f"mkdir $dest/{dirname}")
            for image_id in image_ids:
                print(f"cp $src/{image_id}.jpg $dest/{dirname}")

    def images_pass(self, obs_lists):
        count = 0
        images_per_taxon = self.args.images
        for obs_list in obs_lists:
            label = obs_list[0]['name']
            if label in self.selected_images and len(self.selected_images[label]) >= images_per_taxon:
                continue
            for obs in sorted(obs_list, key=obs_score):
                if -obs_score(obs) < 1.5:
                    break
                if not self.add_next_image(obs, label):
                    break
                count += 1
                if len(self.selected_images[label]) >= images_per_taxon:
                    break
        return count

    def add_next_image(self, obs, label):
        self.selected_images[label] = self.selected_images.get(label, set())
        image_set = self.obs_to_images.get(obs['obs_id'], set())
        if not image_set:
            return False
        thumb_id = obs['image_id']
        if thumb_id in image_set:
            self.selected_images[label].add(thumb_id)
            image_set.remove(thumb_id)
        else:
            self.selected_images[label].add(image_set.pop())
        return True

    def most_common_labels(self, count):
        counts = self.count_labels()
        label_freq = sorted(counts.items(), key=lambda x: -x[1])
        return [elem[0] for elem in label_freq][:count]

    def count_labels(self):
        counts = {}
        for element in self.obs_json:
            name = element['name']
            if ' ' in name and name not in MoArchive.EXCLUSION_LIST:
                counts[name] = counts.get(name, 0) + 1
        return counts

    def obs_by_labels(self, labels):
        by_label = {}
        for element in self.obs_json:
            name = element['name']
            if name in labels:
                by_label[name] = by_label.get(name, [])
                by_label[name].append(element)
        return by_label
            

def _file_labels(filename):
    result = []
    if filename:
        with open(filename) as f:
            for line in f.readlines():
                result.append(line.strip())
    return result

def _obs_to_images(filename, bad_images):
    result = {}
    with open(filename) as file:
        data_reader = csv.reader(file, delimiter="\t")
        next(data_reader)
        for row in data_reader:
            key = int(row[1])
            result[key] = result.get(key, set())
            image_id = int(row[0])
            if image_id not in bad_images:
                result[key].add(image_id)
    return result

def _bad_images(filename):
    result = set()
    with open(filename) as file:
        data_reader = csv.reader(file, delimiter="\t")
        next(data_reader)
        for row in data_reader:
            ok_for_ml = int(row[-1])
            if ok_for_ml == 1:
                continue
            result.add(int(row[0]))
    return result

def obs_score(obs):
    if obs.get('image_id', False):
        return -(obs.get('vote', 0) or 0)
    return 0

def arg_parser():
    parser = argparse.ArgumentParser(description='Generate shell script for creating an archive of MO files')
    parser.add_argument("--label_file", help="File of required labels")
    parser.add_argument("--taxa", help="Desired number of taxa. Default 10.", type=int, default=10)
    parser.add_argument("--images", help="Desired number of images per taxon. Default 10.", type=int, default=10)
    parser.add_argument("--obs_json", help="JSON of observations. Default mo.json", default="mo.json")
    parser.add_argument("--images_csv", help="CSV of images. Default images.csv", default="images.csv")
    parser.add_argument("--images_obs_csv", help="CSV of image to observation mapping. Default images_observations.csv.", default="images_observations.csv")
    return parser.parse_args()

def main():
    archive = MoArchive(arg_parser())
    archive.build()

main()
