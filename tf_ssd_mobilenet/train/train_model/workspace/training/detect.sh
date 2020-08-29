#export CUDA_VISIBLE_DEVICES=1
export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

BASE_PATH=/home/rtml/Documents/weichen/Datasets/CMU/Preprocessing/
TARGET_PATH=set06_L
python detector.py ${BASE_PATH} \
                    ${TARGET_PATH} \
                    ./detection/0827_set06mb1_l_old1

