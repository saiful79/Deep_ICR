#!/usr/bin/python
 # -*- coding: utf-8 -*-

# @ Date      : 09/02/2021
# @ Author    : Md. Saiful Islam
# @ licenses  : MIT

"""
this script work for train and validation for text recogtion module.
you must need image folder and text recogtion annotation txt.

img_folder:
    -img1.jpg
    -img2.jpg

img_folder.txt:
example:
    img1.jpg<space>ground truth
    ---------------------------
    img1.jpg saiful
    img2.jpg saifulbrur79@gmail.com
"""

import os
import shutil
import codecs


file_root_path = "/media/saiful/Educational/deeplearning/dataset/attention_data/" 
output_dir = "/media/saiful/Educational/deeplearning/English_DeepIcr/text_recognition/dataset"

GROUNTH_TRUTH_FILE_NAME = "attation.txt"


DATA_TYPES = ["train","val"]
CLASS_LIST_FILE = os.path.join(output_dir,"class_list.txt")

DISTRBUTION_PERCENTANCE = 20



def get_read_txt_file():
    file_path = os.path.join(file_root_path,GROUNTH_TRUTH_FILE_NAME)
    with open(file_path,"r") as f:
        data = f.read().split("\n")
        data = [i for i in data if i]
        return data

def class_txt_file(data):
    class_list = []
    for files in data:
        img_name, ground_truth = files.split(".jpg ")
        for i in ground_truth:
            if i not in class_list:
                class_list.append(i)
    class_list = sorted(list(set(class_list))) 
    print("Number of Unique Class : ",len(class_list))
    with codecs.open(CLASS_LIST_FILE, 'w', encoding='utf8') as f:
        for char in class_list:
            f.write(char+"\n")
    print(CLASS_LIST_FILE+": Done")
        
def distributed_file(data,data_type):
    data_dir = os.path.join(output_dir,data_type,"gt.txt")
    data_dir_img = os.path.join(output_dir,data_type,"img")
    os.makedirs(data_dir_img,exist_ok=True)
    gt_txt = open(data_dir,"w")
    for files in data:
        img_name, ground_truth = files.split(".jpg ")
        img_path = os.path.join(file_path,"img",img_name+".jpg")
        if os.path.exists(img_path):
            shutil.copy(img_path,data_dir_img)
            gt_txt.write(img_name+".jpg"+" "+ground_truth)
    gt_txt.close()

def get_data_distribution(data):
    total_data = len(data)
    validation_len = (DISTRBUTION_PERCENTANCE*total_data)//100
    train_data = data[validation_len:]
    validation_data = data[:validation_len]
    print(len(train_data))
    print(len(validation_data))
    distributed_file(train_data,DATA_TYPES[0])
    distributed_file(validation_data,DATA_TYPES[1])


if __name__=="__main__":
    data = get_read_txt_file()
    get_data_distribution(data)
    print("Data Distribution :  Done")
    class_txt_file(data)
