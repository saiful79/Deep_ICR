import os
import glob
import math
import cv2
import json
import numpy as np

IS_POLYGON = True

DEBUG = False

CLASS_DICT = {0: 'Text', 1:"other"}
COLORS = {0: (255, 0, 0), 1: (0, 255, 0), 2: (0, 0, 255), 3: (0, 255, 255)}

def read_txt_file(txt_file):
    with open(txt_file,"r", encoding='utf-8', errors='ignore') as f:
        data = f.readlines()
    return data

def read_json(json_path):
    with open(json_path) as f:
        json_data = json.load(f)
    json_data["Invoice_Type"] = "TAX INVOICE"
    json_data["email"] = "email"
    return json_data


def write_json(dataset_dict:dict, json_file_path:str=""):
    """
    save json file
    """
    with open(json_file_path, 'w') as outfile:
        json.dump(dataset_dict, outfile, ensure_ascii=False, indent=4)


def denormalization_coordiante(point_list, constant):
    # print(point_list)
    return [math.floor(float(i)*constant) for i in point_list]


def vgg_format(file_name, size):
    file_format = {
        "filename": file_name,
        "size": size,
        "regions": []
    }
    return file_format

def get_vgg_region_rect(anno_class, text, bbox):
    region = {
        "shape_attributes": {
            "name": "rect",
            "x": int(bbox[0]),
            "y": int(bbox[1]),
            "width": int(bbox[2]),
            "height": int(bbox[3])
        },
        "region_attributes": {
            "Layout": anno_class,
            "Text" : text
        }
    }
    return region

def get_vgg_region_poly(anno_class, entity_name, text, bbox):
    region = {
        "shape_attributes": {
            "name": "polygon",
            "all_points_x": bbox[0],
            "all_points_y": bbox[1],
        },
        "region_attributes": {
            "Layout": anno_class,
            "Text" : text,
            "Entity":entity_name
        }
    }
    return region


def entity_processing(entity_data, text):
    entity_name = [key for key, value in entity_data.items() if text.lower() in value.lower()]
    if len(entity_name)==0:
        entity_name = ["other"]
    return entity_name[0]


    #     print(i)

def get_annotation_format(contents, entity_data, img_file):
    size = os.path.getsize(img_file)
    file_name = os.path.basename(img_file)
    format_data = vgg_format(file_name,  size)
    key = file_name+str(size)
    for elem in contents:
        if elem.strip():
            polygon_bbox, text = elem.split("\n")[0].split(',')[:8], elem.split("\n")[0].split(',')[8:]
            f_text = ",".join(text) 
            # print(polygon_bbox, text)

            all_x = polygon_bbox[::2]  # Extract every other element starting from index 0
            all_y = polygon_bbox[1::2]  # Extract every other element starting from index 1

            # Convert the elements to integers if needed
            all_x = list(map(int, all_x))
            all_y = list(map(int, all_y))

            entity_name = entity_processing(entity_data, f_text)
            

            region = get_vgg_region_poly(CLASS_DICT[0], entity_name, f_text, [all_x, all_y])

            # class_, points = elem.split()[:1][0], elem.split()[1:]
            # region = get_vgg_region_poly(CLASS_DICT[int(class_)], [x, y])

            format_data["regions"].append(region)
        
        # if DEBUG:
        #     x1, y1, x2, y2 = min(x), min(y), max(x), max(y)


        #     cv2.putText(img, CLASS_DICT[int(class_)], (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, \
        #                 COLORS[int(class_)], 1, lineType=cv2.LINE_AA)
        #     if IS_POLYGON:
        #         pts= np.array([[i, j] for i, j in zip(x, y)])
        #         cv2.polylines(img, [pts], True, COLORS[int(class_)], 2)
        #     else:
        #         cv2.rectangle(img, (x1, y1),(x2, y2), COLORS[int(class_)], 2)
    return key, format_data




def processing(img_file, txt_file, entity_path, output_dir):
    data = read_txt_file(txt_file)
    entity_data = read_json(entity_path)
    key, format_data = get_annotation_format(data, entity_data, img_file)
    return key, format_data
        
if __name__ == "__main__" :

    from tqdm import tqdm

    img_file_path = "./test/img"    
    #Annotating a Single Image
    txt_file_path = './test/box'
    entity_path = "./test/entities"

    output_json = "test/vgg_annotation.json"
    output_dir = "logs"
    os.makedirs(output_dir, exist_ok=True)

    files = glob.glob(img_file_path+'/*')
    data_dict = {}
    idx = 0
    for index in tqdm(range(len(files))):
        i = files[index] 
        # try:
        print(f"{i} : {idx} / {len(files)}")
        txt_file = os.path.join(txt_file_path, os.path.basename(i)[:-4]+".txt")
        entity_file = os.path.join(entity_path, os.path.basename(i)[:-4]+".txt")

        key, format_data = processing(
            img_file=i, 
            txt_file=txt_file, 
            entity_path = entity_file, 
            output_dir=output_dir
            )
        data_dict[key] = format_data
        idx += 1
    write_json(data_dict, output_json)

    
 
   

