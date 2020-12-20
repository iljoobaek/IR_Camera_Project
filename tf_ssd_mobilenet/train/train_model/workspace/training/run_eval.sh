export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim
export CUDA_VISIBLE_DEVICES=0

#python eval.py --eval_dir=./eval/eval_faster_rcnn_inception_resnet_v2_CMU00-05-selected_0810/ \
#                --checkpoint_dir=./training/train_faster_rcnn_inception_resnet_v2_CMU00-05-selected_0810/ \
#                --pipeline_config_path=./configs/faster_rcnn_inception_resnet_v2_atrous_coco.config

#python eval.py --eval_dir=./eval/eval_ssd_mobilenet_v2_FLIR_CMU00-05-selected_all_0907/ \
#                --checkpoint_dir=./training/train_ssd_mobilenet_v2_FLIR_CMU00-05-selected_all_0907/ \
#                --pipeline_config_path=./configs/ssd_mobilenet_v2.config

python eval.py --eval_dir=./eval/eval_ssd_mobilenet_v1_FLIR_CMU00-05-selected_all_1220_roi/ \
                --checkpoint_dir=./training/train_ssd_mobilenet_v1_FLIR_CMU00-05-selected_all_1220_roi/ \
                --pipeline_config_path=./configs/ssd_mobilenet_v1.config
