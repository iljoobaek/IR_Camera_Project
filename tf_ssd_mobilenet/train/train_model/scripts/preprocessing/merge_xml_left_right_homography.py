import os
import sys
import cv2
import json

import numpy as np
from numpy.linalg import inv

from xml.etree import ElementTree
import txt2xml


classname = {"car": 0, "pedestrian": 1, "cyclist": 2, "van": 3, "truck": 4, "bus": 5, "animal": 6, "traffic_cone": 7, "channelizer": 8, "person": 1, "bicycle": 2, "dog": 6, "motorcycle": 2}
classind = {0: "car", 1: "pedestrian", 2: "cyclist", 3: "van", 4: "truck", 5: "bus", 6: "animal", 7: "traffic_cone", 8: "channelizer"}


def get_box_from_xml (boxes, xml_path, cnt, h, keep_difficult=False) :
    #boxes = []
    if not os.path.exists(xml_path): return boxes, cnt
    target   = ElementTree.parse(xml_path).getroot()

    for obj in target.iter('object'):

        difficult = int(obj.find('difficult').text) == 1

        if not keep_difficult and difficult:
            continue

        name = obj.find('classname').text.lower().strip()
        bbox = obj.find('bndbox')

        pts    = ['xmin', 'ymin', 'xmax', 'ymax']
        bndbox = []
        #bndbox.append(name)

        for i, pt in enumerate(pts):

            #cur_pt = float(bbox.find(pt).text) - 1
            # scale height or width
            #cur_pt = float(cur_pt) / width if i % 2 == 0 else float(cur_pt) / height

            bndbox.append(float(bbox.find(pt).text))
        #print(bndbox)
        bndbox[0] /= 1280
        bndbox[1] /= 512
        bndbox[2] /= 1280
        bndbox[3] /= 512
        #print(bndbox)
        if name == 'end':
            break
        bbox = txt2xml.Bbox(classind[classname[name]], cnt, [bndbox[1], bndbox[0], bndbox[3], bndbox[2]], difficult)
        cnt += 1
        boxes.append(bbox)
        #bndbox[0] += 0.5
        #bndbox[2] += 0.5
        
        bndbox[0] *= 1280
        bndbox[1] *= 512
        bndbox[2] *= 1280
        bndbox[3] *= 512

        pt1 = np.array([bndbox[0], bndbox[1], 1])
        pt1 = pt1.reshape(3, 1)
        pt2 = np.dot(h, pt1)
        pt2 = pt2 / pt2[2]
        bndbox[0], bndbox[1] = float(pt2[0] + 640), float(pt2[1])

        pt3 = np.array([bndbox[2], bndbox[3], 1])
        pt3 = pt3.reshape(3, 1)
        pt4 = np.dot(h, pt3)
        pt4 = pt4 / pt4[2]
        bndbox[2], bndbox[3] = float(pt4[0] + 640), float(pt4[1])

        bndbox[0] /= 1280
        bndbox[1] /= 512
        bndbox[2] /= 1280
        bndbox[3] /= 512
        #print(bndbox)
        #exit()
        

        bbox = txt2xml.Bbox(classind[classname[name]], cnt, [bndbox[1], bndbox[0], bndbox[3], bndbox[2]], difficult)
        if bndbox[0] >= 0.5:
            boxes.append(bbox)
    return boxes, cnt


def main():
    # if len(sys.argv) < 5:
    #     print("Usage: python combine_xml.py img_path out_path in_path1 in_path2 ...")
    #     exit()
    img_path = sys.argv[1]
    out_path = sys.argv[2]
    in_path = []
    with open("XC90_IR_Stereo.json", "r") as f:
        h_dict = json.load(f)
    h = np.array(h_dict["h"])
    h = inv(h)
    for i in range(3, len(sys.argv)):
        in_path.append(sys.argv[i])
    global_cnt = 0
    # anno_path0 = "../IR_project_ssd_mobilenet/data/VOCdevkit2007/VOC2007/annotation_car_people_bicycle/"
    # anno_path1 = "../IR_project_ssd_mobilenet/data/VOCdevkit2007/VOC2007/annotation_van_truck_bus/"
    # anno_path2 = "../IR_project_ssd_mobilenet/data/VOCdevkit2007/VOC2007/annotation_traffic_cone_channelizer/"
    # out_path = "./xml_labels/"
    # img_path = "../IR_project_ssd_mobilenet/data/VOCdevkit2007/VOC2007/JPEGImages/"
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    anno_path = in_path[0]
    for i_path in sorted(os.listdir(anno_path)):
        boxes = []
        # if not os.path.exists(img_path + i_path.split('.')[0] + '.jpeg'):
        #     print("Not exist")
        # print(img_path + i_path.split('.')[0] + '.jpeg', global_cnt)
        # img = cv2.imread(img_path + i_path.split('.')[0] + '.jpeg')
        # height, width, channels = img.shape
        if 'global' in i_path:
            continue
        name_in = i_path.split('.')[0]
        name = name_in.split('_')
        #name_out = '_'.join(['cmu', 'set05'] + name)
        name_out = '_'.join(name[:2] + name[3:])
        inpath = anno_path + name_in + '.xml'
        outpath = out_path + name_out + '.xml'
        # print(inpath, outpath)
        boxes, global_cnt = get_box_from_xml(boxes, inpath, global_cnt, h)
        # if not os.path.exists(inpath):
        #     print(inpath, "not exist")
        #     continue
        # boxes, global_cnt = get_box_from_xml(boxes, anno_path0 + i_path.split('.')[0] + '.xml', global_cnt)
        # boxes, global_cnt = get_box_from_xml(boxes, anno_path1 + i_path.split('.')[0] + '.xml', global_cnt)
        # boxes, global_cnt = get_box_from_xml(boxes, anno_path2 + i_path.split('.')[0] + '.xml', global_cnt)
        # print(img_path + i_path.split('.')[0] + '.jpeg')
        height, width = 512, 1280
        txt2xml.write_box_to_xml (boxes, out_path, outpath, (height, width), img_path)
        # print(i_path.split('.')[0], global_cnt)


if __name__ == '__main__':
    main()
