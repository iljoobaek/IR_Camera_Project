#export CUDA_VISIBLE_DEVICES=1
export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

BASE_PATH=/home/rtml/Documents/weichen/Datasets/CMU/Preprocessing/
TARGET_PATH=set14_R
python detector.py ${BASE_PATH} \
                    ${TARGET_PATH} \
                    ./detection/0815_setmb_r

