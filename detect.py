'''
python detect.py -i Dev/ -o Result/
'''
import numpy as np
import os
import sys
import tensorflow as tf

from collections import defaultdict
import cv2
import argparse
# from xml.dom.minidom import parse
# import xml.dom.minidom

########Object detection imports########
# sys.path.append("../models/research")
from utils import label_map_util
from utils import visualization_utils as vis_util
# import imutils
# from imutils import contours

parser = argparse.ArgumentParser()
parser.add_argument('-i','--inpath',help = 'the path to folder of input images', required=True)
parser.add_argument('-o','--outpath',help = 'the path to folder of output images', required=True)
# parser.add_argument('-c','--csvpath',help = 'the path to csv ', required=True)
# parser.add_argument('-n','--numImg',help = 'number Image', required=True)
args = parser.parse_args()

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

MODEL_NAME = 'out_graph_dir/saved_model_6000steps'
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
PATH_TO_LABELS = 'object-detection.pbtxt'
NUM_CLASSES = 5
MIN_SCORE_THRESH = 0.7

INPUT_PATH = args.inpath
OUTPUT_PATH = args.outpath
files = os.listdir(INPUT_PATH)

os.environ['CUDA_VISIBLE_DEVICES'] = '0'



# Load a (frozen) Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')
    
########Loading label map########
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)
    

# width = 2592
# height = 1944
# num_pig_detected = 0
#detect

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        for img_num in range(len(files)):
            print(INPUT_PATH + files[img_num])
            img = cv2.imread(INPUT_PATH + files[img_num])
            width = img.shape[1]
            height = img.shape[0]
            

            # Definite input and output Tensors for detection_graph

            # image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            # detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            # num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            image_tensor = 'image_tensor:0'
            detection_boxes = 'detection_boxes:0'
            detection_scores = 'detection_scores:0'
            detection_classes = 'detection_classes:0'
            num_detections = 'num_detections:0'

            RGBframe = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image_np_expanded = np.expand_dims(RGBframe, axis=0)
        
            # Detect      
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})    


            vis_util.visualize_boxes_and_labels_on_image_array(
                img,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                min_score_thresh=.5,
                line_thickness=10)
            indexes = []

            for i in range (classes.size):
                if(classes[0][i] in range(1,91) and scores[0][i]>0.5):
                    indexes.append(i)

            filtered_boxes = boxes[0][indexes, ...]
            filtered_scores = scores[0][indexes, ...]
            filtered_classes = classes[0][indexes, ...]

            # for i in range(0,len(filtered_boxes)):
            #     xmin = width*filtered_boxes[i][1]
            #     xmax = width*filtered_boxes[i][3]
            #     ymin = height*filtered_boxes[i][0]
            #     ymax = height*filtered_boxes[i][2]
                
            #     print('-------------------------------------------------------')
            #     print('xmin: ' + str(xmin))
            #     print('xmax: ' + str(xmax))
            #     print('ymin: ' + str(ymin))
            #     print('ymax: ' + str(ymax))
                
            
            cv2.imwrite(OUTPUT_PATH + files[img_num],img)
            print(OUTPUT_PATH + files[img_num])