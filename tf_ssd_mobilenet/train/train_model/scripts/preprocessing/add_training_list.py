import argparse
import sys
import cv2
import os
from xml.etree import ElementTree

import os.path          as osp
import numpy            as np


def check_num_obj(xml_path):
    if not os.path.exists(xml_path): return 0
    target = ElementTree.parse(xml_path).getroot()
    cnt = 0
    for _ in target.iter('object'): cnt += 1
    return cnt


if __name__ == '__main__' :

    img_path = sys.argv[1]
    anno_path = sys.argv[2]
    out_path = sys.argv[3]

    out_path_train = sys.argv[4]
    out_path_test = sys.argv[5]

    all_images = []
    for name in sorted(os.listdir(img_path)):
        if check_num_obj(osp.join(anno_path, name.split(".")[0] + ".xml")): all_images.append(name)

    # all_images = np.random.permutation(os.listdir(img_path))
    # all_images = np.random.permutation(all_images)
    train_images = all_images[:int(0.8 * len(all_images))]
    test_images = all_images[int(0.8 * len(all_images)):]
    with open(out_path, 'w+') as f:
        for name in all_images:
            f.write(name.split(".")[0] + '\n')
    with open(out_path_train, 'w+') as f:
        for name in train_images:
            f.write(name.split(".")[0] + '\n')
    with open(out_path_test, 'w+') as f:
        for name in test_images:
            f.write(name.split(".")[0] + '\n')
    
    print(len(all_images))
    print("Done!")
