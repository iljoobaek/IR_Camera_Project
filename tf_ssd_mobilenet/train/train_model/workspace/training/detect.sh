export CUDA_VISIBLE_DEVICES=0
export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

BASE_PATH=/home/rtml/Documents/weichen/Datasets/CMU/Preprocessing/
TARGET_PATH=setxx_cmu00-05-selected_split2
python detector.py ${BASE_PATH} \
                    ${TARGET_PATH} \
                    ./detection/0808_setxx_cmu00-05-selected_split2

