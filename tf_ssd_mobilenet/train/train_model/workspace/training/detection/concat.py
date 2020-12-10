import cv2
import numpy as np
import os

img_dir1 = '0827_set25mb1_rr_1129'
img_dir2 = '0827_set25mb1_rl_1129'

img_dir_out = 'out_rr_rl'

if not os.path.exists(img_dir_out):
    os.mkdir(img_dir_out)

for f in sorted(os.listdir(img_dir1)):
    img1 = os.path.join(img_dir1, f)
    img2 = os.path.join(img_dir2, f)
    im1 = cv2.imread(img1)
    im2 = cv2.imread(img2)

    im_v = cv2.hconcat([im1, im1])
    outpath = os.path.join(img_dir_out, f)
    cv2.imwrite(outpath, im_v)

