export CUDA_VISIBLE_DEVICES=1
export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

BASE_PATH=../../../Datasets/CMU/Preprocessing/
TARGET_PATH=setxx1
python detector.py ${BASE_PATH} \
                    ${TARGET_PATH} \
                    ./detection/0713_flir_cmu05

