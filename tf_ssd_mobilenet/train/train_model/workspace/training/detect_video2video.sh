#export CUDA_VISIBLE_DEVICES=1
export PYTHONPATH=$PYTHONPATH:../../models/research/:../../models/research/slim

VIDEO_PATH=/home/rtml/Downloads/schenley_park_sep_20/schenley_park_cmu_area.avi
python detector_video2video.py ${VIDEO_PATH} \
                    ./detection/videos/schenley_park_cmu_area.avi

