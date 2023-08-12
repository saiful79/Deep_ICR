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

def block_region_format(bbox:dict={}, text:str="") ->dict:
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
                "text":text
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
    line_structure_data = file_formate(file_name, size)
    word_structure_data = file_formate(file_name, size)
    region_data = data["recognitionResults"]
    # print(region_data)
    for i in region_data[0]["lines"]:
        print(i)
        boundingBox, text  = i["boundingBox"], i["text"]
        all_x, all_y = boundingBox[::2], boundingBox[1::2]

        line_bbox = [min(all_x), min(all_y), max(all_x), max(all_y)]

        line_data = block_region_format(line_bbox, text)

        line_structure_data["regions"].append(line_data)

        for word in i["words"]:
            boundingBox, text  = word["boundingBox"], word["text"]
            all_x, all_y = boundingBox[::2], boundingBox[1::2]
            word_bbox = [min(all_x), min(all_y), max(all_x), max(all_y)]

            word_data = block_region_format(word_bbox, text)
            word_structure_data["regions"].append(word_data)

    return line_structure_data, word_structure_data, key


if __name__ == "__main__":

    annotation_data = "/media/sayan/hdd1/DATASET/DOCVQA/train/ocr_results"
    image_data = "/media/sayan/hdd1/DATASET/DOCVQA/train/documents"
    image_data_files = glob.glob(image_data+"/*")

    line_dict, word_dict = {}, {}
    for f in image_data_files:
        file_name = os.path.basename(f)

        json_file = os.path.join(annotation_data, file_name[:-4]+".json")
        data = read_json(json_file)
        # print(data)
        # break
        line_structure_data, word_structure_data, key = docvaq2vgg_format(
            img_path=f, 
            data=data, 
            file_name=file_name
            )
        # break

        line_dict[key] = line_structure_data
        word_dict[key] = word_structure_data

    write_json(line_dict, "vgg_line_test.json")
    write_json(word_dict, "vgg_word_test.json")

