import os
import json
import cv2
import random
from shapely.geometry import Polygon
import glob

DEBUG = True

def write_json(dataset_dict:dict, json_file_path:str=""):
    """
    save json file
    """
    with open(json_file_path, 'w') as outfile:
        json.dump(dataset_dict, outfile, ensure_ascii=False, indent=4)
   
def read_json(json_path:str='')->dict:
    """
    json file reading
    """
    with open(json_path) as json_file:
        data = json.load(json_file)
    return data

def block_region_format(bbox:dict={}, text:str="", category="", group_id="") ->dict:
    x, y, w, h = bbox[0], bbox[1], abs(bbox[2]-bbox[0]), abs(bbox[3]-bbox[1]) 
    region = {
        "shape_attributes": {
            "name": "rect",
            "x": x,
            "y": y,
            "width": w,
            "height": h
            },
        "region_attributes": {
                "layout": "Text",
                "text": text,
                "category": category,
                "group_id": group_id
            }
        }
    return region

def file_formate(file_name:str="", size :int= "")-> dict:
    file_structure = {
        "filename": file_name,
        "size": size,
        "regions": []
        }
    return file_structure




def docvaq2vgg_format(img_path, data, file_name):

    size = os.path.getsize(img_path)

    key = file_name+str(size)
    # line_structure_data = file_formate(file_name, size)
    word_structure_data = file_formate(file_name, size)
    
    region_data = data["valid_line"]

    for words in region_data:
        print(words)
        category, group_id = words["category"], words["group_id"]
        print(category)
        for w_q in words["words"]:
            w = w_q["quad"]
            box, text = [w["x1"], w["y1"], w["x2"], w["y2"], w["x3"], w["y3"], w["x4"], w["y4"]], w_q["text"]
            all_x, all_y = box[::2], box[1::2]
            bbox = [box[0], box[1], max(all_x), max(all_y)]
            word_data = block_region_format(bbox, text, category, group_id)
            word_structure_data["regions"].append(word_data)

    return word_structure_data, key


if __name__ == "__main__":

    annotation_data = "/media/sayan/hdd1/DATASET/CORD/CORD-20230715T053906Z-001/CORD/dev/json"
    image_data = "/media/sayan/hdd1/DATASET/CORD/CORD-20230715T053906Z-001/CORD/dev/image"
    image_data_files = glob.glob(image_data+"/*")

    line_dict, word_dict = {}, {}
    for f in image_data_files:

        file_name = os.path.basename(f)

        print("file_name", file_name)

        json_file = os.path.join(annotation_data, file_name[:-4]+".json")
        data = read_json(json_file)
        word_structure_data, key = docvaq2vgg_format(
            img_path=f, 
            data=data, 
            file_name=file_name
            )
        word_dict[key] = word_structure_data

        print("============================================")

    # write_json(line_dict, "vgg_line_test.json")
    write_json(word_dict, "vgg_word_test.json")

