export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

EVAL_DIR=../../workspace/training/eval/eval_20200713
EVAL_RESULT_PATH=${EVAL_DIR}/results.csv
IMAGE_DIR=config/data/cmudata/JPEGImages/set00
OUT_DIR=config/data/cmudata/JPEGImages/set00_eval_metrics/prediction/
ANNO_DIR=config/data/cmudata/JPEGImages/set00_eval_metrics/annotation/
THRESHOLD=0.5

#mkdir -p ${OUT_DIR}

python draw_eval_results.py ${EVAL_RESULT_PATH} ${IMAGE_DIR} ${OUT_DIR} ${ANNO_DIR} ${THRESHOLD}
