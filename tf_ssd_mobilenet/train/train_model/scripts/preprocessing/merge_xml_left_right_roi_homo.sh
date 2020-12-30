export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim
# env: tfmobile_py2
BASE_PATH=/home/droid/Documents/weichen/Datasets/CMU
IMG_PATH=${BASE_PATH}/Preprocessing/Images/set_merged_roi/
OUT_PATH=${BASE_PATH}/Preprocessing/Annotations/set_merged_roi_homo/
IN_PATH1=${BASE_PATH}/Preprocessing/Annotations/set05_L/
#IN_PATH1=/home/droid/Documents/weichen/Datasets/FLIR/Preprocessing/Annotations/FLIR/
#IN_PATH2=${BASE_PATH}/Preprocessing/Annotations/annotation_traffic_cone_channelizer/
#IN_PATH3=${BASE_PATH}/Preprocessing/Annotations/annotation_van_truck_bus/
python merge_xml_left_right_roi_homo.py ${IMG_PATH} ${OUT_PATH} ${IN_PATH1}
