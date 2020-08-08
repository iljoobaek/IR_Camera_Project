export CUDA_VISIBLE_DEVICES=0
export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

BASE_PATH=/home/rtml/Documents/weichen/Datasets/CMU/Preprocessing/
TARGET_PATH=set14_L
python detector.py ${BASE_PATH} \
                    ${TARGET_PATH} \
                    ./detection/0808_cmu14_nof

