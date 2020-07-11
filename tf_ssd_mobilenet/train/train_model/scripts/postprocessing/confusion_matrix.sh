export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim
BASE=../../workspace/training/

python confusion_matrix.py --detections_record=${BASE}training/test_detections.tfrecord --label_map=${BASE}training/cmudata_label_map.pbtxt --output_path=${BASE}eval/confusion_matrix.csv
