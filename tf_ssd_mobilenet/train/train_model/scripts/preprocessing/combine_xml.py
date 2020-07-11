import os
import sys
import cv2

from xml.etree import ElementTree
import txt2xml


classname = {"car": 0, "pedestrian": 1, "cyclist": 2, "van": 3, "truck": 4, "bus": 5, "animal": 6, "traffic_cone": 7, "channelizer": 8, "person": 1, "bicycle": 2, "dog": 6}
classind = {0: "car", 1: "pedestrian", 2: "cyclist", 3: "van", 4: "truck", 5: "bus", 6: "animal", 7: "traffic_cone", 8: "channelizer"}


def get_box_from_xml (boxes, xml_path, cnt, keep_difficult=False) :
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
        bndbox[2] = bndbox[2] - bndbox[0]
        bndbox[3] = bndbox[3] - bndbox[1]
        #print(bndbox)
        bbox = txt2xml.Bbox(classind[classname[name]], cnt, bndbox, difficult)
        cnt += 1
        boxes.append(bbox)
    return boxes, cnt


def main():
    if len(sys.argv) < 5:
        print("Usage: python combine_xml.py img_path out_path in_path1 in_path2 ...")
        exit()
    img_path = sys.argv[1]
    out_path = sys.argv[2]
    in_path = []
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
    for i_path in sorted(os.listdir(img_path)):
        boxes = []
        for anno_path in in_path:
            boxes, global_cnt = get_box_from_xml(boxes, anno_path + i_path.split('.')[0] + '.xml', global_cnt)
        # boxes, global_cnt = get_box_from_xml(boxes, anno_path0 + i_path.split('.')[0] + '.xml', global_cnt)
        # boxes, global_cnt = get_box_from_xml(boxes, anno_path1 + i_path.split('.')[0] + '.xml', global_cnt)
        # boxes, global_cnt = get_box_from_xml(boxes, anno_path2 + i_path.split('.')[0] + '.xml', global_cnt)
        # print(img_path + i_path.split('.')[0] + '.jpeg')
        img    = cv2.imread(img_path + i_path.split('.')[0] + '.jpeg')
        height, width, channels = img.shape
        txt2xml.write_box_to_xml (boxes, out_path, out_path + i_path.split('.')[0] + '.xml', (height, width), img_path)
        print(i_path.split('.')[0], global_cnt)


if __name__ == '__main__':
    main()
