import cv2
import sys
import os

if len(sys.argv) == 2:
    directory = sys.argv[1]

pic_list = os.listdir(directory)
i = 0

while True:
    
    key = cv2.waitKey(0)
    
    if key == ord('0'):
        while pic_list[i].split("_")[0] != '0':
            i += 1 
            if i == len(pic_list):
                i = 0

    elif key == ord('1'):
        while pic_list[i].split("_")[0] != '1':
            i += 1 
            if i == len(pic_list):
                i = 0
       
    elif key == ord('2'):
        while pic_list[i].split("_")[0] != '2':
            i += 1 
            if i == len(pic_list):
                i = 0

    elif key == ord('3'):
        while pic_list[i].split("_")[0] != '3':
            i += 1 
            if i == len(pic_list):
                i = 0

    elif key == ord('4'):
        while pic_list[i].split("_")[0] != '4':
            i += 1 
            if i == len(pic_list):
                i = 0

    elif key != 27:
        i += 1 
        if i == len(pic_list):
            i = 0

    else:
        cv2.destroyAllWindows()
        break

    image = cv2.imread(os.path.join(directory, pic_list[i]), 0);
    resized_image = cv2.resize(image, (1920, 1080))
    
    win_name = "label = " + pic_list[i].split("_")[0]
    cv2.imshow(win_name, resized_image)


