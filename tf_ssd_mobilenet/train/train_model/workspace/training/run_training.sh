export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

python train.py --train_dir=./training/train_ssd_mobilenet_v1_FLIR_CMU00-05/ --pipeline_config_path=./configs/ssd_mobilenet_v1.config
