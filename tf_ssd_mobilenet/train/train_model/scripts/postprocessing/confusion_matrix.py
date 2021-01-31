import functools
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

from object_detection.core import standard_fields
from object_detection.metrics import tf_example_parser
from object_detection.utils import label_map_util
from object_detection.builders import dataset_builder
from object_detection.utils import config_util

flags = tf.app.flags

flags.DEFINE_string('label_map', None, 'Path to the label map')
flags.DEFINE_string('detections_record', None, 'Path to the detections record file')
flags.DEFINE_string('detections_record2', None, 'Path to the detections record file')
flags.DEFINE_string('output_path', None, 'Path to the output the results in a csv.')
flags.DEFINE_string('pipeline_config_path', None, 'Path to the output the results in a csv.')

FLAGS = flags.FLAGS

IOU_THRESHOLD = 0.5
CONFIDENCE_THRESHOLD = 0.5

def compute_iou(groundtruth_box, detection_box):
    g_ymin, g_xmin, g_ymax, g_xmax = tuple(groundtruth_box.tolist())
    d_ymin, d_xmin, d_ymax, d_xmax = tuple(detection_box.tolist())
    
    xa = max(g_xmin, d_xmin)
    ya = max(g_ymin, d_ymin)
    xb = min(g_xmax, d_xmax)
    yb = min(g_ymax, d_ymax)

    intersection = max(0, xb - xa + 1) * max(0, yb - ya + 1)

    boxAArea = (g_xmax - g_xmin + 1) * (g_ymax - g_ymin + 1)
    boxBArea = (d_xmax - d_xmin + 1) * (d_ymax - d_ymin + 1)

    return intersection / float(boxAArea + boxBArea - intersection)

def process_detections(detections_record, categories):
    record_iterator = tf.python_io.tf_record_iterator(path=detections_record)
    data_parser = tf_example_parser.TfExampleDetectionAndGTParser()

    # configs = config_util.get_configs_from_pipeline_file(FLAGS.pipeline_config_path)
    # input_config = configs['eval_input_config']
    #
    # def get_next(config):
    #     return dataset_builder.make_initializable_iterator(
    #         dataset_builder.build(config)).get_next()
    #
    # create_input_dict_fn = functools.partial(get_next, input_config)

    confusion_matrix = np.zeros(shape=(len(categories) + 1, len(categories) + 1))

    image_index = 0
    for string_record in record_iterator:
        example = tf.train.Example()
        example.ParseFromString(string_record)
        decoded_dict = data_parser.parse(example)

        # print(decoded_dict)
        
        image_index += 1
        
        if decoded_dict:
            groundtruth_boxes = decoded_dict[standard_fields.InputDataFields.groundtruth_boxes]
            groundtruth_classes = decoded_dict[standard_fields.InputDataFields.groundtruth_classes]
            
            detection_scores = decoded_dict[standard_fields.DetectionResultFields.detection_scores]
            detection_classes = decoded_dict[standard_fields.DetectionResultFields.detection_classes][detection_scores >= CONFIDENCE_THRESHOLD]
            detection_boxes = decoded_dict[standard_fields.DetectionResultFields.detection_boxes][detection_scores >= CONFIDENCE_THRESHOLD]
            
            matches = []
            
            if image_index % 100 == 0:
                print("Processed %d images" %(image_index))
            
            for i in range(len(groundtruth_boxes)): #9
                for j in range(len(detection_boxes)): #100
                    iou = compute_iou(groundtruth_boxes[i], detection_boxes[j])
                    
                    if iou > IOU_THRESHOLD:
                        matches.append([i, j, iou])
                    
            matches = np.array(matches)
            if matches.shape[0] > 0:
                # Sort list of matches by descending IOU so we can remove duplicate detections
                # while keeping the highest IOU entry.
                matches = matches[matches[:, 2].argsort()[::-1][:len(matches)]]
                
                # Remove duplicate detections from the list.
                matches = matches[np.unique(matches[:,1], return_index=True)[1]]
                
                # Sort the list again by descending IOU. Removing duplicates doesn't preserve
                # our previous sort.
                matches = matches[matches[:, 2].argsort()[::-1][:len(matches)]]
                
                # Remove duplicate ground truths from the list.
                matches = matches[np.unique(matches[:,0], return_index=True)[1]]
                
            for i in range(len(groundtruth_boxes)):
                if matches.shape[0] > 0 and matches[matches[:,0] == i].shape[0] == 1:
                    confusion_matrix[groundtruth_classes[i] - 1][detection_classes[int(matches[matches[:,0] == i, 1][0])] - 1] += 1 
                else:
                    confusion_matrix[groundtruth_classes[i] - 1][confusion_matrix.shape[1] - 1] += 1
                    
            for i in range(len(detection_boxes)):
                if matches.shape[0] > 0 and matches[matches[:,1] == i].shape[0] == 0:
                    confusion_matrix[confusion_matrix.shape[0] - 1][detection_classes[i] - 1] += 1
        else:
            print("Skipped image %d" % (image_index))

    print("Processed %d images" % (image_index))

    return confusion_matrix

def bboxes_sort(classes, scores, bboxes, top_k=400):
    """Sort bounding boxes by decreasing order and keep only the top_k
    """
    # if priority_inside:
    #     inside = (bboxes[:, 0] > margin) & (bboxes[:, 1] > margin) & \
    #         (bboxes[:, 2] < 1-margin) & (bboxes[:, 3] < 1-margin)
    #     idxes = np.argsort(-scores)
    #     inside = inside[idxes]
    #     idxes = np.concatenate([idxes[inside], idxes[~inside]])
    idxes = np.argsort(-scores)
    classes = classes[idxes][:top_k]
    scores = scores[idxes][:top_k]
    bboxes = bboxes[idxes][:top_k]
    return classes, scores, bboxes

def bboxes_jaccard(bboxes1, bboxes2):
    """Computing jaccard index between bboxes1 and bboxes2.
    Note: bboxes1 and bboxes2 can be multi-dimensional, but should broacastable.
    """
    bboxes1 = np.transpose(bboxes1)
    bboxes2 = np.transpose(bboxes2)
    # Intersection bbox and volume.
    int_ymin = np.maximum(bboxes1[0], bboxes2[0])
    int_xmin = np.maximum(bboxes1[1], bboxes2[1])
    int_ymax = np.minimum(bboxes1[2], bboxes2[2])
    int_xmax = np.minimum(bboxes1[3], bboxes2[3])

    int_h = np.maximum(int_ymax - int_ymin, 0.)
    int_w = np.maximum(int_xmax - int_xmin, 0.)
    int_vol = int_h * int_w
    # Union volume.
    vol1 = (bboxes1[2] - bboxes1[0]) * (bboxes1[3] - bboxes1[1])
    vol2 = (bboxes2[2] - bboxes2[0]) * (bboxes2[3] - bboxes2[1])
    jaccard = int_vol / (vol1 + vol2 - int_vol)
    return jaccard

def bboxes_nms(classes, scores, bboxes, nms_threshold=0.45):
    """Apply non-maximum selection to bounding boxes.
    """
    keep_bboxes = np.ones(scores.shape, dtype=np.bool)
    for i in range(scores.size-1):
        if keep_bboxes[i]:
            # Computer overlap with bboxes which are following.
            overlap = bboxes_jaccard(bboxes[i], bboxes[(i+1):])
            # Overlap threshold for keeping + checking part of the same class
            keep_overlap = np.logical_or(overlap < nms_threshold, classes[(i+1):] != classes[i])
            keep_bboxes[(i+1):] = np.logical_and(keep_bboxes[(i+1):], keep_overlap)##

    idxes = np.where(keep_bboxes)
    return classes[idxes], scores[idxes], bboxes[idxes]

def process_detections_2(detections_record1, detections_record2, categories):
    record_iterator1 = tf.python_io.tf_record_iterator(path=detections_record1)
    record_iterator2 = tf.python_io.tf_record_iterator(path=detections_record2)
    data_parser = tf_example_parser.TfExampleDetectionAndGTParser()

    # configs = config_util.get_configs_from_pipeline_file(FLAGS.pipeline_config_path)
    # input_config = configs['eval_input_config']
    #
    # def get_next(config):
    #     return dataset_builder.make_initializable_iterator(
    #         dataset_builder.build(config)).get_next()
    #
    # create_input_dict_fn = functools.partial(get_next, input_config)

    confusion_matrix = np.zeros(shape=(len(categories) + 1, len(categories) + 1))
    all_gt_boxes = []
    all_gt_classes = []
    all_detect_scores = []
    all_detect_classes = []
    all_detect_boxes = []

    image_index = 0
    for string_record in record_iterator1:
        example = tf.train.Example()
        example.ParseFromString(string_record)
        decoded_dict = data_parser.parse(example)

        # print(decoded_dict)

        image_index += 1

        if decoded_dict:
            groundtruth_boxes = decoded_dict[standard_fields.InputDataFields.groundtruth_boxes]
            groundtruth_classes = decoded_dict[standard_fields.InputDataFields.groundtruth_classes]
            all_gt_boxes.append(groundtruth_boxes)
            all_gt_classes.append(groundtruth_classes)

            detection_scores = decoded_dict[standard_fields.DetectionResultFields.detection_scores]
            detection_classes = decoded_dict[standard_fields.DetectionResultFields.detection_classes]
            detection_boxes = decoded_dict[standard_fields.DetectionResultFields.detection_boxes]
            # detection_classes = decoded_dict[standard_fields.DetectionResultFields.detection_classes][
            #     detection_scores >= CONFIDENCE_THRESHOLD]
            # detection_boxes = decoded_dict[standard_fields.DetectionResultFields.detection_boxes][
            #     detection_scores >= CONFIDENCE_THRESHOLD]
            all_detect_scores.append(detection_scores)
            all_detect_classes.append(detection_classes)
            all_detect_boxes.append(detection_boxes)
            # print(type(detection_scores), type(detection_classes), type(detection_boxes))
            # print(detection_scores.shape, detection_classes.shape, detection_boxes.shape)
            # exit()

        else:
            print("Skipped image %d" % (image_index))

    image_index = 0
    for string_record in record_iterator2:
        example = tf.train.Example()
        example.ParseFromString(string_record)
        decoded_dict = data_parser.parse(example)

        # print(decoded_dict)

        if decoded_dict:
            # print(all_detect_scores[image_index].shape, all_detect_classes[image_index].shape,
            #       all_detect_boxes[image_index].shape)

            detection_scores = decoded_dict[standard_fields.DetectionResultFields.detection_scores]
            detection_classes = decoded_dict[standard_fields.DetectionResultFields.detection_classes]
            detection_boxes = decoded_dict[standard_fields.DetectionResultFields.detection_boxes]
            # detection_classes = decoded_dict[standard_fields.DetectionResultFields.detection_classes][
            #     detection_scores >= CONFIDENCE_THRESHOLD]
            # detection_boxes = decoded_dict[standard_fields.DetectionResultFields.detection_boxes][
            #     detection_scores >= CONFIDENCE_THRESHOLD]
            all_detect_scores[image_index] = np.append(all_detect_scores[image_index], detection_scores, 0)
            all_detect_classes[image_index] = np.append(all_detect_classes[image_index], detection_classes, 0)
            all_detect_boxes[image_index] = np.append(all_detect_boxes[image_index], detection_boxes, 0)
            # print(all_detect_scores[image_index].shape, all_detect_classes[image_index].shape, all_detect_boxes[image_index].shape)
            # exit()

        else:
            print("Skipped image %d" % (image_index))
        image_index += 1

    for idx in range(len(all_gt_boxes)):

        detection_scores = all_detect_scores[idx]
        detection_classes = all_detect_classes[idx]
        detection_boxes = all_detect_boxes[idx]
        groundtruth_boxes = all_gt_boxes[idx]
        groundtruth_classes = all_gt_classes[idx]
        # print(detection_scores.shape, detection_classes.shape, detection_boxes.shape)
        detection_classes, detection_scores, detection_boxes = bboxes_sort(detection_classes, detection_scores, detection_boxes, 100)
        detection_classes, detection_scores, detection_boxes = bboxes_nms(detection_classes, detection_scores,
                                                                          detection_boxes)
        detection_boxes = detection_boxes[detection_scores >= CONFIDENCE_THRESHOLD]
        detection_classes = detection_classes[detection_scores >= CONFIDENCE_THRESHOLD]

        matches = []

        if idx % 100 == 0:
            print("Processed %d images" % (image_index))

        for i in range(len(groundtruth_boxes)):  # 9
            for j in range(len(detection_boxes)):  # 100
                iou = compute_iou(groundtruth_boxes[i], detection_boxes[j])

                if iou > IOU_THRESHOLD:
                    matches.append([i, j, iou])

        matches = np.array(matches)
        if matches.shape[0] > 0:
            # Sort list of matches by descending IOU so we can remove duplicate detections
            # while keeping the highest IOU entry.
            matches = matches[matches[:, 2].argsort()[::-1][:len(matches)]]

            # Remove duplicate detections from the list.
            matches = matches[np.unique(matches[:, 1], return_index=True)[1]]

            # Sort the list again by descending IOU. Removing duplicates doesn't preserve
            # our previous sort.
            matches = matches[matches[:, 2].argsort()[::-1][:len(matches)]]

            # Remove duplicate ground truths from the list.
            matches = matches[np.unique(matches[:, 0], return_index=True)[1]]

        for i in range(len(groundtruth_boxes)):
            if matches.shape[0] > 0 and matches[matches[:, 0] == i].shape[0] == 1:
                confusion_matrix[groundtruth_classes[i] - 1][
                    detection_classes[int(matches[matches[:, 0] == i, 1][0])] - 1] += 1
            else:
                confusion_matrix[groundtruth_classes[i] - 1][confusion_matrix.shape[1] - 1] += 1

        for i in range(len(detection_boxes)):
            if matches.shape[0] > 0 and matches[matches[:, 1] == i].shape[0] == 0:
                confusion_matrix[confusion_matrix.shape[0] - 1][detection_classes[i] - 1] += 1

    print("Processed %d images" % (idx))

    return confusion_matrix


def process_detections3(detections_record, categories):
    record_iterator = tf.python_io.tf_record_iterator(path=detections_record)
    data_parser = tf_example_parser.TfExampleDetectionAndGTParser()

    confusion_matrix = np.zeros(shape=(len(categories) + 1, len(categories) + 1))

    image_index = 0
    for string_record in record_iterator:
        example = tf.train.Example()
        example.ParseFromString(string_record)
        decoded_dict = data_parser.parse(example)

        # print(decoded_dict)

        image_index += 1

        if decoded_dict:
            groundtruth_boxes = decoded_dict[standard_fields.InputDataFields.groundtruth_boxes]
            groundtruth_classes = decoded_dict[standard_fields.InputDataFields.groundtruth_classes]

            detection_scores = decoded_dict[standard_fields.DetectionResultFields.detection_scores]
            detection_classes = decoded_dict[standard_fields.DetectionResultFields.detection_classes][
                detection_scores >= CONFIDENCE_THRESHOLD]
            detection_boxes = decoded_dict[standard_fields.DetectionResultFields.detection_boxes][
                detection_scores >= CONFIDENCE_THRESHOLD]

            # remove half of groundtruth boxes
            # map right bbox from right to left
            print(groundtruth_boxes)
            print(groundtruth_boxes.shape, detection_boxes.shape)
            exit()

            matches = []

            if image_index % 100 == 0:
                print("Processed %d images" % (image_index))

            for i in range(len(groundtruth_boxes)):  # 9
                for j in range(len(detection_boxes)):  # 100
                    iou = compute_iou(groundtruth_boxes[i], detection_boxes[j])

                    if iou > IOU_THRESHOLD:
                        matches.append([i, j, iou])

            matches = np.array(matches)
            if matches.shape[0] > 0:
                # Sort list of matches by descending IOU so we can remove duplicate detections
                # while keeping the highest IOU entry.
                matches = matches[matches[:, 2].argsort()[::-1][:len(matches)]]

                # Remove duplicate detections from the list.
                matches = matches[np.unique(matches[:, 1], return_index=True)[1]]

                # Sort the list again by descending IOU. Removing duplicates doesn't preserve
                # our previous sort.
                matches = matches[matches[:, 2].argsort()[::-1][:len(matches)]]

                # Remove duplicate ground truths from the list.
                matches = matches[np.unique(matches[:, 0], return_index=True)[1]]

            for i in range(len(groundtruth_boxes)):
                if matches.shape[0] > 0 and matches[matches[:, 0] == i].shape[0] == 1:
                    confusion_matrix[groundtruth_classes[i] - 1][
                        detection_classes[int(matches[matches[:, 0] == i, 1][0])] - 1] += 1
                else:
                    confusion_matrix[groundtruth_classes[i] - 1][confusion_matrix.shape[1] - 1] += 1

            for i in range(len(detection_boxes)):
                if matches.shape[0] > 0 and matches[matches[:, 1] == i].shape[0] == 0:
                    confusion_matrix[confusion_matrix.shape[0] - 1][detection_classes[i] - 1] += 1
        else:
            print("Skipped image %d" % (image_index))

    print("Processed %d images" % (image_index))

    return confusion_matrix


def display(confusion_matrix, categories, output_path):
    print("\nConfusion Matrix:")
    # print(confusion_matrix, "\n")
    for r in confusion_matrix:
        print(", ".join([str(n) for n in r]) + "\n")
    results = []

    for i in range(len(categories)):
        id = categories[i]["id"] - 1
        name = categories[i]["name"]
        
        total_target = np.sum(confusion_matrix[id,:])
        total_predicted = np.sum(confusion_matrix[:,id])
        
        precision = float(confusion_matrix[id, id] / total_predicted)
        recall = float(confusion_matrix[id, id] / total_target)
        
        #print('precision_{}@{}IOU: {:.2f}'.format(name, IOU_THRESHOLD, precision))
        #print('recall_{}@{}IOU: {:.2f}'.format(name, IOU_THRESHOLD, recall))
        
        results.append({'category' : name, 'precision_@{}IOU'.format(IOU_THRESHOLD) : precision, 'recall_@{}IOU'.format(IOU_THRESHOLD) : recall})
    
    df = pd.DataFrame(results)
    print(df)
    df.to_csv(output_path)
    
def main(argv):
    del argv
    required_flags = ['detections_record', 'label_map', 'output_path']
    for flag_name in required_flags:
        if not getattr(FLAGS, flag_name):
            raise ValueError('Flag --{} is required'.format(flag_name))

    label_map = label_map_util.load_labelmap(FLAGS.label_map)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=100, use_display_name=True)

    # confusion_matrix = process_detections(FLAGS.detections_record, categories)
    confusion_matrix = process_detections3(FLAGS.detections_record, categories)
    #confusion_matrix = process_detections_2(FLAGS.detections_record, FLAGS.detections_record2, categories)

    display(confusion_matrix, categories, FLAGS.output_path)    
    
if __name__ == '__main__':
    tf.app.run(main)
