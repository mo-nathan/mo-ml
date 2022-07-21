# Build archive of 100 taxa with 100 images
# mo.json, images_observations.csv
# 100 most common species names
# 100 images, select first image from each reasonable obs (vote_cache > 1.5)
# then fill in with additional passes

import sys
import json
import csv

class MoArchive:
    EXCLUSION_LIST = ['Mixed collection']

    def __init__(self, obs_filename, images_filename):
        with open(obs_filename) as json_file:
            self.obs_json = json.load(json_file)
        with open(images_filename) as csv_file:
            self.obs_to_images = _obs_to_images(images_filename)
        self.selected_images = {} # label => Set of images_ids

    def build(self, taxon_count, images_per_taxon):
        labels = self.most_common_labels(taxon_count)
        obs_lists = self.obs_by_labels(labels).values()
        images_found = 1
        count = 0
        while images_found > 0:
            images_found = self.images_pass(obs_lists, images_per_taxon)
            count += images_found
        self.print_script()

    def print_script(self):
        for label, image_ids in self.selected_images.items():
            dirname = label.replace(' ', '_')
            print(f"mkdir $dest/{dirname}")
            for image_id in image_ids:
                print(f"cp $src/{image_id}.jpg $dest/{dirname}")

    def images_pass(self, obs_lists, images_per_taxon):
        count = 0
        for obs_list in obs_lists:
            label = obs_list[0]['name']
            if label in self.selected_images and len(self.selected_images[label]) >= images_per_taxon:
                continue
            for obs in sorted(obs_list, key=obs_score):
                if -obs_score(obs) < 2.0:
                    break
                if self.add_next_image(obs, label):
                    count += 1
                if len(self.selected_images[label]) >= images_per_taxon:
                    break
        return count

    def add_next_image(self, obs, label):
        self.selected_images[label] = self.selected_images.get(label, set())
        if obs['image_id'] in self.selected_images[label]:
            for image_id in self.obs_to_images[obs['obs_id']]:
                if image_id not in self.selected_images[label]:
                    self.selected_images[label].add(image_id)
                    return True
        else:
            self.selected_images[label].add(obs['image_id'])
            return True
        return False

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
            
def _obs_to_images(filename):
    result = {}
    with open(filename) as file:
        data_reader = csv.reader(file, delimiter="\t")
        next(data_reader)
        for row in data_reader:
            key = int(row[1])
            result[key] = result.get(key, [])
            result[key].append(int(row[0]))
    return result

def obs_score(obs):
    if obs.get('image_id', False):
        return -(obs.get('vote', 0) or 0)
    return 0

def main():
    archive = MoArchive("mo.json", "images_observations.csv")
    archive.build(int(sys.argv[1]), int(sys.argv[2]))

main()
