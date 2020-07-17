export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

python eval.py --eval_dir=./eval/eval_faster_rcnn_inception_resnet_v2_FLIR_CMU00-05/ \
                --checkpoint_dir=./training/train_faster_rcnn_inception_resnet_v2_FLIR_CMU00-05/ \
                --pipeline_config_path=./configs/faster_rcnn_inception_resnet_v2_atrous_coco.config
