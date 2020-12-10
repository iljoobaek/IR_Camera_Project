import os
import sys
import codecs
from copy import deepcopy
import cv2
import pandas as pd

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree


class Bbox(object):
    """ The defination of bbox class"""
    def __init__(self, classname, object_id, box, difficult, visible=True, score=0):
        """
        Arg:
            classname: the name of object class
            object_id: the unique id for this object
            bbox: (xmin, ymin, width, height)
            kwargs: optinal arguments, such as difficult
        """
        self.classname = classname
        self.object_id = object_id
        self.box = box
        self.difficult = difficult
        self.visible = visible
        self.score = score

def mergeBboxes(bboxes, bboxes_prev):
    """ This function merges two sets of bboxes based on unique ids.
    If an id exists in both bboxes and bboxes_prev, the bbox in bboxes
    will be chosen but the tracked box's visibility will follow.
    """
    bboxes_merged = deepcopy(bboxes)
    for bbox in bboxes_prev:
        is_exist = False
        for bbox_merged in bboxes_merged:
            if bbox.object_id == bbox_merged.object_id:
                is_exist = True
                bbox_merged.visible = bbox.visible
                break
        if not is_exist:
            bboxes_merged.append(bbox)
    return bboxes_merged

class TrackedBbox(object):
    """ The defination of tracked bbox class """
    def __init__(self, bbox, image, tracker_type='MEDIANFLOW'):
        (major_ver,minor_ver,subminor_ver)=(cv2.__version__).split('.')
        tracker_types = ['BOOSTING', 'MIL','KCF', 'MEDIANFLOW']
        # 'TLD' and GOTURN not working this moment
        # tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
        assert tracker_type in tracker_types, "tracker type not supported"
        if int(minor_ver) < 3:
            tracker = cv2.Tracker_create(tracker_type)
        else:
            if tracker_type == 'BOOSTING':
                tracker = cv2.TrackerBoosting_create()
            if tracker_type == 'MIL':
                tracker = cv2.TrackerMIL_create()
            if tracker_type == 'KCF':
                tracker = cv2.TrackerKCF_create()
            if tracker_type == 'TLD':
                tracker = cv2.TrackerTLD_create()
            if tracker_type == 'MEDIANFLOW':
                tracker = cv2.TrackerMedianFlow_create()
            if tracker_type == 'GOTURN':
                tracker = cv2.TrackerGOTURN_create()
        self.tracker_type = tracker_type
        self.tracker = tracker
        self.bbox = bbox

        # Initialize tracker with first frame and bounding box
        ok = self.tracker.init(image, bbox.box)
        assert ok, "can not initialize tracker"
    def update(self, image):
        ok, box = self.tracker.update(image)
        if ok:
            self.bbox.box = box
            print('tracked box visibility')
            print(self.bbox.visible)
            return self.bbox
        print('tracking failed for object id %d' % self.bbox.object_id)
        return self.bbox


XML_EXT = '.xml'
ENCODE_METHOD = 'utf-8'
class MotWriter:
    """ The class of annotation reading and writing in multiple object tracking
    format. """
    def __init__(self, foldername, filename, imgSize,
                databaseSrc='Unknown', localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        return etree.tostring(
            root,
            pretty_print=True,
            encoding=ENCODE_METHOD).replace("  ".encode(), "\t".encode())
        # minidom does not support UTF-8
        '''reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t", encoding=ENCODE_METHOD)'''

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = Element('annotation')
        if self.verified:
            top.set('verified', 'yes')

        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        if self.localImgPath is not None:
            localImgPath = SubElement(top, 'path')
            localImgPath.text = self.localImgPath

        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = self.databaseSrc

        size_part = SubElement(top, 'size')
        width = SubElement(size_part, 'width')
        height = SubElement(size_part, 'height')
        depth = SubElement(size_part, 'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize) == 3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def addBbox(self, bbox):
        #print(bbox)
        #xmin, ymin, w, h = bbox.box
        xmin, ymin, xmax, ymax = bbox.box
        ymin, xmin, ymax, xmax = bbox.box
        #print(xmin, ymin, w, h)
        bndbox = {'xmin': xmin * self.imgSize[1], 'ymin': ymin * self.imgSize[0], 'xmax': xmax * self.imgSize[1], 'ymax': ymax * self.imgSize[0]}
        bndbox['classname'] = bbox.classname
        bndbox['object_id'] = bbox.object_id
        bndbox['difficult'] = bbox.difficult
        bndbox['score'] = bbox.score
        self.boxlist.append(bndbox)

    def appendObjects(self, top):
        for each_object in self.boxlist:
            object_item = SubElement(top, 'object')
            classname = SubElement(object_item, 'classname')
            try:
                classname.text = unicode(each_object['classname'])
            except NameError:
                # Py3: NameError: name 'unicode' is not defined
                classname.text = each_object['classname']
            object_id = SubElement(object_item, 'object_id')
            object_id.text = str(each_object['object_id'])
            truncated = SubElement(object_item, 'truncated')
            if int(each_object['ymax']) == int(self.imgSize[0]) or (int(each_object['ymin'])== 1):
                truncated.text = "1" # max == height or min
            elif (int(each_object['xmax'])==int(self.imgSize[1])) or (int(each_object['xmin'])== 1):
                truncated.text = "1" # max == width or min
            else:
                truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = str( bool(each_object['difficult']) & 1 )
            score = SubElement(object_item, 'score')
            score.text = str(each_object['score'])
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])

    def save(self, targetFile=None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                self.filename + XML_EXT, 'w', encoding=ENCODE_METHOD)
        else:
            out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)

        prettifyResult = self.prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()


class GlobalWriter:
    """ The class of annotation reading and writing in multiple object tracking
    format. """
    def __init__(self, nextId):
        self.nextId = nextId

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        return etree.tostring(
            root,
            pretty_print=True,
            encoding=ENCODE_METHOD).replace("  ".encode(), "\t".encode())
        # minidom does not support UTF-8
        '''reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="\t", encoding=ENCODE_METHOD)'''

    def genXML(self):
        """
            Return XML root
        """
        top = Element('annotation')
        nextId = SubElement(top, 'nextId')
        nextId.text = str(self.nextId)
        return top

    def save(self, targetFile):
        assert targetFile.endswith(XML_EXT), "Unsupport save format"
        root = self.genXML()
        out_file = codecs.open(targetFile, 'w', encoding=ENCODE_METHOD)
        prettifyResult = self.prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()

classname = {"car": 0, "pedestrian": 1, "cyclist": 2, "van": 3, "truck": 4, "bus": 5, "animal": 6, "traffic_cone": 7, "channnelizer": 8}
classind = {0: "car", 1: "pedestrian", 2: "cyclist", 3: "van", 4: "truck", 5: "bus", 6: "animal", 7: "traffic_cone", 8: "channnelizer"}


def write_box_to_xml (boxes, fileFolder, filename, shape, imagePath):
    writer = MotWriter(fileFolder, filename, shape, localImgPath=imagePath)
    for bbox in boxes:
        writer.addBbox(bbox)
    writer.save(targetFile=filename)


# def main():
# 	anno_path = sys.argv[1]
# 	out_path = sys.argv[2]
# 	img_path = sys.argv[3]
# 	global_cnt = 0
# 	for i_path in sorted(os.listdir(anno_path)):
# 		boxes, global_cnt = get_box_from_txt(anno_path + i_path, global_cnt)
# 		img    = cv2.imread(img_path + i_path.split('.')[0] + '.jpeg')
# 		height, width, channels = img.shape
# 		write_box_to_xml (boxes, out_path, out_path + i_path.split('.')[0] + '.xml', (height, width), img_path)
# 		print(global_cnt)
# 	glbwriter = GlobalWriter(global_cnt)
# 	glbwriter.save(out_path + 'global_nextId.xml')
#
#
# if __name__ == '__main__':
# 	main()
