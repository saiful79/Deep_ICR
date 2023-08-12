import os
import json
import cv2
import glob
import random
from shapely.geometry import Polygon

# image contain image list
IMAGE_FOLDER = "images"
# json contain vgg annotation formate with text class
JOSN_NAME = "data.json"

# CORD_DATA_PATH = "/media/sayan/hdd1/DATASET/layout_detection_data/CORD"
# DOCVQA  = "/media/sayan/hdd1/DATASET/layout_detection_data/DOCVQA"
# FUNSD =  "/media/sayan/hdd1/DATASET/layout_detection_data/funsd_dataset"

aug_data = "/media/sayan/hdd1/DATASET/upwork_data/augment_data"
upwork_data = "/media/sayan/hdd1/DATASET/upwork_data/pdf_editable"

# DATA_TYPE = ["train", "val", "test"]
DATA_TYPE = ["train"]
# DATA_PATH = [CORD_DATA_PATH, DOCVQA, FUNSD]
DATA_PATH = [aug_data, upwork_data]

DEBUG = True

OUTPUT_DIR = "../OCR_TEXT_DATA/images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_GT = "../OCR_TEXT_DATA/gt_2.txt"


def read_json(json_path:str='')->dict:
    """
    json file reading
    """
    with open(json_path) as json_file:
        data = json.load(json_file)
    return data
index = 2394050
with open(OUTPUT_GT, "w") as f:
    for d_p in DATA_PATH:
        for i in DATA_TYPE:
            print("Data path:", d_p, i)
            json_path = os.path.join(d_p, i, JOSN_NAME)
            # image_path = os.path.join(d_p, i, IMAGE_FOLDER)
            data = read_json(json_path)
            # print(data)
            for key, value in data.items():
                filename =value["filename"]
                regions = value["regions"]
                image_path = os.path.join(d_p, i, IMAGE_FOLDER, filename)
                image = cv2.imread(image_path)
                for r in regions:
                    print(r)
                    try:
                        shape_attributes = r["shape_attributes"]
                        region_attributes = r["region_attributes"]["text"]
                        if "�" in region_attributes:
                            continue
                        x, y, w, h = shape_attributes["x"], shape_attributes["y"], shape_attributes["width"], shape_attributes["height"]
                        x1, y1, x2, y2 = x, y, x+w, y+h
                        crop_img_name = filename[:-4]+"_"+str(index)+".jpg"
                        output_crop_img_path = os.path.join(OUTPUT_DIR, crop_img_name)
                        cropped_image = image[y1:y2, x1:x2]
                        cv2.imwrite(output_crop_img_path, cropped_image)
                        f.write(crop_img_name+"\t"+region_attributes+"\n")
                        index += 1
                    except:
                        continue 
                # {'shape_attributes': {'name': 'rect', 'x': 1325, 'y': 2569, 'width': 477, 'height': 81}, 'region_attributes': {'layout': 'Text', 'text': '113,886', 'category': 'total.total_price', 'group_id': 6}}



