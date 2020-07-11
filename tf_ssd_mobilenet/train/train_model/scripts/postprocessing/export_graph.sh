export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

INPUT_TYPE=image_tensor
PIPELINE_CONFIG_PATH=../../workspace/training/configs/ssd_mobilenet_v1.config
TRAINED_CKPT_PREFIX=../../workspace/training/training/train_ssd_mobilenet_v1/model.ckpt-97165
EXPORT_DIR=../../workspace/training/exported_models/froze_graph_0617/
python export_inference_graph.py \
    --input_type=${INPUT_TYPE} \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --trained_checkpoint_prefix=${TRAINED_CKPT_PREFIX} \
    --output_directory=${EXPORT_DIR}