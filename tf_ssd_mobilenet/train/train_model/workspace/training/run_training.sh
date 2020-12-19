export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

python train.py --train_dir=./training/train_ssd_mobilenet_v1_FLIR_CMU00-05-selected_all_1219_homo/ \
                --pipeline_config_path=./configs/ssd_mobilenet_v1.config \

#python train.py --train_dir=./training/train_ssd_mobilenet_v2_FLIR_CMU00-05-selected_all_0907/ \
#                --pipeline_config_path=./configs/ssd_mobilenet_v2.config \

#python train.py --train_dir=./training/train_faster_rcnn_inception_resnet_v2_CMU00-05-selected_0811/ \
#                --pipeline_config_path=./configs/faster_rcnn_inception_resnet_v2_atrous_coco.config \
