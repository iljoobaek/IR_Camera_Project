export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

EVAL_DIR=../../workspace/training/eval/eval_20200615
IN_PATH=../../workspace/training/training/test_detections.tfrecord
EVAL_CONFIG_PATH=${EVAL_DIR}/eval_config.pbtxt
INPUT_CONFIG_PATH=${EVAL_DIR}/input_config.pbtxt
RESULT_PATH=${EVAL_DIR}/results.csv

mkdir -p ${EVAL_DIR}

echo "
label_map_path: '../../workspace/training/training/cmudata_label_map.pbtxt'
tf_record_input_reader: { input_path: '${IN_PATH}' }
" > ${INPUT_CONFIG_PATH}

echo "
metrics_set: 'pascal_voc_detection_metrics'
" > ${EVAL_CONFIG_PATH}

python -m offline_eval_map_corloc \
  --eval_dir=${EVAL_DIR} \
  --eval_config_path=${EVAL_CONFIG_PATH} \
  --input_config_path=${INPUT_CONFIG_PATH} \
  --result_path=${RESULT_PATH}
