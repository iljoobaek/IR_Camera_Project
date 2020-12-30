export CUDA_VISIBLE_DEVICES=1
export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

BASE_PATH=/home/rtml/Documents/weichen/Datasets/CMU/Preprocessing/
TARGET_PATH=setxx3_L
python detector_l_r.py ${BASE_PATH} \
                    ${TARGET_PATH} \
                    ./detection/set25mb1_setxx3_rr

