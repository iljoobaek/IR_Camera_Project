# env: tfmobile_py2
BASE_PATH=../Datasets/FLIR/
IMG_PATH=${BASE_PATH}JPEGImages/
OUT_PATH=${BASE_PATH}/Preprocessing/Annotations/annotations/
IN_PATH1=${BASE_PATH}/Preprocessing/Annotations/annotation_car_people_bicycle/
IN_PATH2=${BASE_PATH}/Preprocessing/Annotations/annotation_traffic_cone_channelizer/
IN_PATH3=${BASE_PATH}/Preprocessing/Annotations/annotation_van_truck_bus/
python combine_xml.py ${IMG_PATH} ${OUT_PATH} ${IN_PATH1} ${IN_PATH2} ${IN_PATH3}