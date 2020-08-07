export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim
export CUDA_VISIBLE_DEVICES=1

#python eval.py --eval_dir=./eval/eval_faster_rcnn_inception_resnet_v2_FLIR_CMU00-05/ \
#                --checkpoint_dir=./training/train_faster_rcnn_inception_resnet_v2_FLIR_CMU00-05/ \
#                --pipeline_config_path=./configs/faster_rcnn_inception_resnet_v2_atrous_coco.config

python eval.py --eval_dir=./eval/eval_ssd_mobilenet_v1_CMU00-05-selected/ \
                --checkpoint_dir=./training/train_ssd_mobilenet_v1_CMU00-05-selected/ \
                --pipeline_config_path=./configs/ssd_mobilenet_v1.config
