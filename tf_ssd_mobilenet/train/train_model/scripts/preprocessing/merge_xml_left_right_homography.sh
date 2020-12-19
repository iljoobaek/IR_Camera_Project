export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim
# env: tfmobile_py2
BASE_PATH=/home/droid/Documents/weichen/Datasets/CMU
IMG_PATH=${BASE_PATH}/Preprocessing/Images/set_merged/
OUT_PATH=${BASE_PATH}/Preprocessing/Annotations/set_merged_homo/
IN_PATH1=${BASE_PATH}/Preprocessing/Annotations/set_selected/
#IN_PATH2=${BASE_PATH}/Preprocessing/Annotations/annotation_traffic_cone_channelizer/
#IN_PATH3=${BASE_PATH}/Preprocessing/Annotations/annotation_van_truck_bus/
python merge_xml_left_right_homography.py ${IMG_PATH} ${OUT_PATH} ${IN_PATH1}
