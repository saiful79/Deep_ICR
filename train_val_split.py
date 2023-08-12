import os 
import glob
import shutil

output_="dataset"
os.makedirs(output_,exist_ok=True)


def image_move_and_txt(data,type_,root):
    # os.makedirs(type_,exist_ok=True) 
    img_path = output_+"/"+type_+"/img"
    os.makedirs(img_path,exist_ok=True)
    txt = open(output_+"/"+type_+"/gt.txt","w") 
    for i in data:
        image,label= i.split(".jpg ")
        txt_save_image= image+".jpg"

        image = root+"/img/"+image+".jpg"
        if label == "\u200c" or label == "\u200d":
            continue
        if os.path.exists(image):
            print()
            shutil.copy(image,img_path)
            if label:
                txt.write(txt_save_image+" "+label+"\n")
            print(i)
    txt.close()



def main(data_path):
    annotation_path = data_path+"/data.txt"
    print(annotation_path)
    with open(annotation_path,"r") as file_:
        data = file_.read().split("\n")
        print(data)
        val = int((len(data)*20)/100)
        image_move_and_txt(data[val:],"train",data_path)
        image_move_and_txt(data[:val],"val",data_path)
if __name__=="__main__":
    data_path="/home/saiful/Desktop/LCD_text_detection/text-recognition/lcd_data"
    main(data_path)
    
