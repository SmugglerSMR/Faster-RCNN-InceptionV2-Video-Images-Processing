import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

import os, cv2
from tqdm import tqdm
import animal_size_determination
import collections
import moviepy.editor as mp

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = 'detection/output/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'detection/label.pbtxt'

NUM_CLASSES = 2

# Colours for drawing
STANDARD_COLORS = [
    'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
    'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen'
]


detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


def load_image_into_numpy_array(image, h, w):
    #(im_width, im_height) = image.size
    im_width = w
    im_height = h
    return np.array(image).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

# Detection code
# For range has to be set by number of images appeared in testing graph.
PATH_TO_TEST_IMAGES_DIR = 'test'
TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'st{}.jpg'.format(i)) for i in range(1, 7) ]

# Size, in inches, of the output images.
IMAGE_SIZE = (12, 8)

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def resize_video(video_inp):
    clip = mp.VideoFileClip(video_inp)
    clip_resized = clip.resize(height=320, width=240) # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
    #clip.
    clip_resized.write_videofile("ProcessedStuff/movie_resized.mp4")

def detection_code(video_inp):
    resize_video(video_inp)
    video_out = 'ProcessedStuff/predicted.mp4'
    video_original = 'ProcessedStuff/original.mp4'
    video_reader = cv2.VideoCapture('ProcessedStuff/movie_resized.mp4')
    # Check if camera opened successfully
    if (video_reader.isOpened()== False): 
        print("Error opening video stream or file")

    file = open("ProcessedStuff/labels_example.txt","w") 
    file.close()

    nb_frames = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))    
    frame_h = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_w = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    # frame_h = 320
    # frame_w = 240
    # Set sizis manually
    #out_h = 600
    #out_w = 717
    print(frame_h)
    print(frame_w)
    video_writer = cv2.VideoWriter(video_out,
                                cv2.VideoWriter_fourcc(*'mp4v'), 
                                28.0, 
                                (frame_w, frame_h))
    
    video_writer_original = cv2.VideoWriter(video_original,
                                cv2.VideoWriter_fourcc(*'mp4v'), 
                                28.0, 
                                (frame_w, frame_h))


    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            skip_frame = 1
            skipt_each_n = 6
            for i in tqdm(range(int(nb_frames/skipt_each_n)-1)):
                ret, frame = video_reader.read()        
                if skip_frame == skipt_each_n:
                    skip_frame = 1
                    for i in range(1, skipt_each_n-1):
                        ret, frame = video_reader.read()                                       
                    #ret, frame = video_reader.read()                                       
                skip_frame = skip_frame + 1
                original_frame = frame
                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.
                image_np = load_image_into_numpy_array(frame, frame_h, frame_w)
                image_np_original = load_image_into_numpy_array(original_frame, frame_h, frame_w)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np = cv2.resize(image_np, (frame_w, frame_h), interpolation = cv2.INTER_AREA)
                # original_image = image_np

                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                # height, width = image_np_expanded.shape[:2]
                
                
                # Run detection
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                # Visualization of the results of a detection.
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    min_score_thresh=.95,
                    groundtruth_box_visualization_color='black',
                    line_thickness=3)
                
                video_writer.write(np.uint8(image_np))
                video_writer_original.write(np.uint8(image_np_original))
                # Detecting sizes                
                # Getting information: Practicing
                box_to_color_map = collections.defaultdict(str)
                nb_count = 0
                boxes = np.squeeze(boxes)
                scores = np.squeeze(scores)
                classes = np.squeeze(classes).astype(np.int32)
                for i in range(min(20, boxes.shape[0])):
                    if scores is None or scores[i] > 0.94:                        
                        nb_count = nb_count+1
                for i in range(min(20, boxes.shape[0])):
                    if scores is None or scores[i] > 0.94:
                        box = tuple(boxes[i].tolist())
                        box_to_color_map[box] = 'black'
                        box_to_color_map[box] = STANDARD_COLORS[
                            classes[i] % len(STANDARD_COLORS)]
                        ymin, xmin, ymax, xmax = box
                        # Multiple with image height and width
                        class_name = category_index[classes[i]]['id']
                        width_px = xmax*frame_w-xmin*frame_w
                        animal_size_determination.animal_get_size(width_px, class_name, nb_frames, nb_count)
            
            print('Video released')
            print(int(video_writer.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            print(int(video_writer.get(cv2.CAP_PROP_FRAME_WIDTH)))
            video_reader.release()
            video_writer.release()
            video_writer_original.release()

# # Provides a start point for out code
# if __name__ == "__main__":
#     detection_code()