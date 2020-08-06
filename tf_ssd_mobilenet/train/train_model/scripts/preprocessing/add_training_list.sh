# env: tfmobile_py2
BASE_PATH=../../../../../Datasets/CMU/
NAME=set_selected
IMG_PATH=${BASE_PATH}Preprocessing/Images/${NAME}/
ANNO_PATH=${BASE_PATH}Preprocessing/Annotations/${NAME}/
OUT_PATH_all=${BASE_PATH}Preprocessing/ImageLists/${NAME}.txt
OUT_PATH_train=${BASE_PATH}Preprocessing/ImageLists/${NAME}_train.txt
OUT_PATH_test=${BASE_PATH}Preprocessing/ImageLists/${NAME}_test.txt
python add_training_list.py ${IMG_PATH} ${ANNO_PATH} ${OUT_PATH_all} ${OUT_PATH_train} ${OUT_PATH_test}