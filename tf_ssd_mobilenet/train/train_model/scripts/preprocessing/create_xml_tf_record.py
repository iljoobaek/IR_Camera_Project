# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

r"""Convert raw PASCAL dataset to TFRecord for object_detection.

Example usage:
    python object_detection/dataset_tools/create_pascal_tf_record.py \
        --data_dir=/home/user/VOCdevkit \
        --year=VOC2012 \
        --output_path=/home/user/pascal.record
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import hashlib
import io
import logging
import os

from lxml import etree
import PIL.Image
import tensorflow as tf

from object_detection.utils import dataset_util
from object_detection.utils import label_map_util


flags = tf.app.flags
# flags.DEFINE_string('data_dir', 'CMU/', 'Root directory to raw PASCAL VOC dataset.')
#flags.DEFINE_string('set', 'train', 'Convert training set, validation set or '
#                    'merged set.')
# flags.DEFINE_string('annotations_dir', 'annotations',
                    # '(Relative) path to annotations directory.')
# flags.DEFINE_string('year', 'VOC2007', 'Desired challenge year.')
# flags.DEFINE_string('output_path', 'combined_train.record', 'Path to output TFRecord')
flags.DEFINE_string('type', 'train', 'train or test')
flags.DEFINE_string('label_map_path', '../../workspace/training/training/cmudata_label_map.pbtxt',
                    'Path to label map proto')
flags.DEFINE_boolean('ignore_difficult_instances', False, 'Whether to ignore '
                     'difficult instances')
FLAGS = flags.FLAGS

#SETS = ['train', 'val', 'trainval', 'test']
#YEARS = ['VOC2007', 'VOC2012', 'merged']
cnt = {}


def dict_to_tf_example(data, filename,
                       dataset_directory,
                       label_map_dict,
                       ignore_difficult_instances=False,
                       image_subdirectory='JPEGImages'):
  """Convert XML derived dict to tf.Example proto.

  Notice that this function normalizes the bounding box coordinates provided
  by the raw data.

  Args:
    data: dict holding PASCAL XML fields for a single image (obtained by
      running dataset_util.recursive_parse_xml_to_dict)
    dataset_directory: Path to root directory holding PASCAL dataset
    label_map_dict: A map from string label names to integers ids.
    ignore_difficult_instances: Whether to skip difficult instances in the
      dataset  (default: False).
    image_subdirectory: String specifying subdirectory within the
      PASCAL dataset directory holding the actual image data.

  Returns:
    example: The converted tf.Example.

  Raises:
    ValueError: if the image pointed to by data['filename'] is not a valid JPEG
  """
  img_path = os.path.join(image_subdirectory, filename + ".jpeg")
  full_path = os.path.join(dataset_directory, img_path)
  with tf.gfile.GFile(full_path, 'rb') as fid:
    encoded_jpg = fid.read()
  encoded_jpg_io = io.BytesIO(encoded_jpg)
  image = PIL.Image.open(encoded_jpg_io)
  if image.format != 'JPEG':
    raise ValueError('Image format not JPEG')
  key = hashlib.sha256(encoded_jpg).hexdigest()

  width = int(data['size']['width'])
  height = int(data['size']['height'])

  id_to_classname = {1: "car", 2: "pedestrian", 3: "cyclist", 4: "van", 5: "truck",
                     6: "bus", 7: "animal", 8: "traffic_cone", 9: "channelizer",
                     0: "background"}

  xmin = []
  ymin = []
  xmax = []
  ymax = []
  classes = []
  classes_text = []
  truncated = []
  # poses = []
  difficult_obj = []
  if 'object' in data:
    for obj in data['object']:
      difficult = bool(int(obj['difficult']))
      if ignore_difficult_instances and difficult:
        continue

      difficult_obj.append(int(difficult))

      xmin.append(float(obj['bndbox']['xmin']) / width)
      ymin.append(float(obj['bndbox']['ymin']) / height)
      xmax.append(float(obj['bndbox']['xmax']) / width)
      ymax.append(float(obj['bndbox']['ymax']) / height)
      # classes_text.append(obj['classname'].encode('utf8'))
      classes_text.append(id_to_classname[label_map_dict[obj['classname']]].encode('utf8'))
      classes.append(label_map_dict[obj['classname']])
      truncated.append(int(obj['truncated']))

      if label_map_dict[obj['classname']] in cnt:
        cnt[label_map_dict[obj['classname']]] += 1
      else:
        cnt[label_map_dict[obj['classname']]] = 1
      # poses.append(obj['pose'].encode('utf8'))

  example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(
          data['filename'].encode('utf8')),
      'image/source_id': dataset_util.bytes_feature(
          data['filename'].encode('utf8')),
      'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
      'image/encoded': dataset_util.bytes_feature(encoded_jpg),
      'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
      'image/object/difficult': dataset_util.int64_list_feature(difficult_obj),
      'image/object/truncated': dataset_util.int64_list_feature(truncated),
      # 'image/object/view': dataset_util.bytes_list_feature(poses),
  }))
  return example


def main(_):
  # data_dir = FLAGS.data_dir
  output_path = '../../workspace/training/training/' + FLAGS.type + '.tfrecord'
  writer = tf.python_io.TFRecordWriter(output_path)

  label_map_dict = label_map_util.get_label_map_dict(FLAGS.label_map_path)
  label_map_dict['person'] = 2
  label_map_dict['bicycle'] = 3
  label_map_dict['motorcycle'] = 3
  label_map_dict['END'] = 0
  # label_map_dict['bicycle'] = 0
  # label_map_dict['motorcycle'] = 0
  # label_map_dict['cyclist'] = 0
  # label_map_dict['van'] = 1
  # label_map_dict['truck'] = 1
  # label_map_dict['bus'] = 1
  # label_map_dict['animal'] = 0
  # label_map_dict['traffic_cone'] = 0
  # label_map_dict['channelizer'] = 0
  # print(label_map_dict)
  # exit()
  data_dirs = {"FLIR": "/home/rtml/Documents/weichen/Datasets/FLIR/",
               "set00": "/home/rtml/Documents/weichen/Datasets/CMU/",
               "set01": "/home/rtml/Documents/weichen/Datasets/CMU/",
               "set02": "/home/rtml/Documents/weichen/Datasets/CMU/",
               "set03": "/home/rtml/Documents/weichen/Datasets/CMU/",
               "set04": "/home/rtml/Documents/weichen/Datasets/CMU/",
               "set05_L": "/home/rtml/Documents/weichen/Datasets/CMU/",
               "set_selected": "/home/rtml/Documents/weichen/Datasets/CMU/",
               #"setxx_cmu00-05-selected_split2": "/home/rtml/Documents/weichen/Datasets/CMU/",
               }

  cnt_img = 0
  for data_dir in data_dirs:
      logging.info('Reading from %s dataset.', data_dir)
      examples_path = os.path.join(data_dirs[data_dir], 'Preprocessing', 'ImageLists', data_dir + '_' + FLAGS.type + '.txt')
      annotations_dir = os.path.join(data_dirs[data_dir], 'Preprocessing', 'Annotations', data_dir)
      examples_list = dataset_util.read_examples_list(examples_path)
      for idx, example in enumerate(examples_list):
        cnt_img += 1
        if idx % 100 == 0:
          logging.info('On image %d of %d', idx, len(examples_list))
        path = os.path.join(annotations_dir, example + '.xml')
        # print(path)
        with tf.gfile.GFile(path, 'r') as fid:
          xml_str = fid.read()
        xml = etree.fromstring(xml_str)
        data = dataset_util.recursive_parse_xml_to_dict(xml)['annotation']

        tf_example = dict_to_tf_example(data, example, data_dirs[data_dir], label_map_dict,
                                        FLAGS.ignore_difficult_instances, image_subdirectory='Preprocessing/Images/' + data_dir)
        writer.write(tf_example.SerializeToString())

  writer.close()
  print(cnt_img, cnt)


if __name__ == '__main__':
  tf.app.run()
