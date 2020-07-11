export CUDA_VISIBLE_DEVICES=1
export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

BASE_PATH=../../../Datasets/FLIR/Preprocessing/
TARGET_PATH=FLIR
python detector.py ${BASE_PATH} \
                    ${TARGET_PATH} \
                    ./detection

