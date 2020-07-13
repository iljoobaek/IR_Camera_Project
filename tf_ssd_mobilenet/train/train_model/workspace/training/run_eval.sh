export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

python eval.py --eval_dir=./eval/eval_ssd_mobilenet_v1_FLIR_CMU05/ --checkpoint_dir=./training/train_ssd_mobilenet_v1_FLIR_CMU05/ --pipeline_config_path=./configs/ssd_mobilenet_v1.config
