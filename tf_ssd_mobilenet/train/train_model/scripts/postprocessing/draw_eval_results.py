import sys
import cv2
import pandas as pd
import os
import tensorflow as tf
import txt2xml

eval_result_file = sys.argv[1]
image_dir = sys.argv[2]
output_dir = sys.argv[3]
annotation_dir = sys.argv[4]
threshold = float(sys.argv[5])

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
if not os.path.exists(annotation_dir):
    os.mkdir(annotation_dir)

r = pd.read_csv(eval_result_file, delimiter=",", names=["ImageID", "Class", "Prob", "x1", "y1", "x2", "y2"])
r['x1'] = r['x1'].astype(float)
r['y1'] = r['y1'].astype(float)
r['x2'] = r['x2'].astype(float)
r['y2'] = r['y2'].astype(float)
classind = {1: "car", 2: "pedestrian", 3: "cyclist", 4: "van", 5: "truck", 6: "bus", 7: "animal", 8: "traffic_cone", 9: "channelizer"}
colormap = {1: (255, 128, 0), 2: (0, 0, 255), 3: (51, 153, 255), 4: (255, 229, 204), 5: (255, 153, 204), 6: (255, 0, 255), 7: (0, 76, 153), 8: (0, 255, 128), 9: (102, 204, 0)}

processed_images = 0
processed_boxes = 0
for image_id, g in r.groupby('ImageID'):
    tf.compat.v1.logging.log_every_n(tf.compat.v1.logging.INFO, 'Processed %d images...', 1000,
                           processed_images)
    processed_images += 1
    image = cv2.imread(os.path.join(image_dir, image_id + ".jpeg"))
    height, width, channels = image.shape
    boxes = []
    for row in g.itertuples():
        if row.Prob < threshold:
            continue
        # cv2.rectangle(image, (int(row.x1 * width), int(row.y1 * height)), (int(row.x2 * width), int(row.y2 * height)), (255, 255, 0), 4)
        cv2.rectangle(image, (int(row.x1 * width), int(row.y1 * height)), (int(row.x2 * width), int(row.y2 * height)),
                      colormap[row.Class], 4)
        label = "%s: %.2f" % (classind[row.Class], row.Prob)
        cv2.putText(image, label,
                    (int(row.x1 * width) + 2, int(row.y1 * height) + 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,  # font scale
                    (255, 0, 255),
                    2)  # line type

        bndbox = [row.x1 * width, row.y1 * height, row.x2 * width - row.x1 * width, row.y2 * height - row.y1 * height]
        bbox = txt2xml.Bbox(classind[row.Class], processed_boxes, bndbox, False)
        boxes.append(bbox)
        processed_boxes += 1
    cv2.imwrite(os.path.join(output_dir, image_id + ".jpeg"), image)
    txt2xml.write_box_to_xml(boxes, annotation_dir, annotation_dir + image_id + ".xml", (height, width), os.path.join(image_dir, image_id + ".jpeg"))
glbwriter = txt2xml.GlobalWriter(processed_boxes)
glbwriter.save(annotation_dir + 'global_nextId.xml')
print("Task Done. Processed %d images." % (processed_images,))
