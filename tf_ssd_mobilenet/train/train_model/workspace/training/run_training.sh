export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

python train.py --train_dir=./training/train_ssd_mobilenet_v1_CMU00-05-selected_different/ \
                --pipeline_config_path=./configs/ssd_mobilenet_v1.config \

#python train.py --train_dir=./training/train_faster_rcnn_inception_resnet_v2_FLIR_CMU00-05/ \
#                --pipeline_config_path=./configs/faster_rcnn_inception_resnet_v2_atrous_coco.config \
