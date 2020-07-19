export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

SPLIT=../../workspace/training/training/test_detections.tfrecord  # or test
#TF_RECORD_FILES=$(ls -1 ${SPLIT}_tfrecords/* | tr '\n' ',')
TF_RECORD_FILES=../../workspace/training/training/test.tfrecord
INF_DIR=../../workspace/training/exported_models/froze_graph_0719/frozen_inference_graph.pb

PYTHONPATH=$PYTHONPATH:$(readlink -f ..) \
python -m infer_detections \
  --input_tfrecord_paths=$TF_RECORD_FILES \
  --output_tfrecord_path=${SPLIT} \
  --inference_graph=$INF_DIR \
  --discard_image_pixels