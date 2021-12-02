#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 13:00:10 2021

@author: Sam

Function: transfor 'yolo format' to 'rectangle format' for calculate mAP

reference: https://blog.csdn.net/weixin_43508499/article/details/118600392
"""
import glob
import os
import cv2

# classna,e
cls_file = './dog_cat_monkey/obj_names.txt'
with open(cls_file, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

def get_basename(filepath):
    '''
        filename and extension name
        filepath = '/home/ubuntu/python/example.py'
        return basename = example.py
    '''
    return os.path.basename(filepath)

def get_filename_only(filepath):
    '''filepath = '/home/ubuntu/python/example.py'
       return filename = example
    '''
    basename = os.path.basename(filepath)
    return os.path.splitext(basename)[0]  

def created_directory(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def isfile(f):
    '''Check if the file exists
       input filepath
       return True/False
    '''
    if os.path.isfile(f):
       return True
    else:
       return False

def yolo_to_retangle(temp, w, h):
    '''
    imput yolo format and img' weight and height
    return retangle format x1, x2, y1, y2
    <class_name> <0-left> <1-top> <2-right> <3-bottom> [<difficult>]
    '''
    x_, y_, w_, h_=eval(temp[1]), eval(temp[2]), eval(temp[3]), eval(temp[4])
    x1 = w * x_ - 0.5 * w * w_
    x2 = w * x_ + 0.5 * w * w_
    y1 = h * y_ - 0.5 * h * h_
    y2 = h * y_ + 0.5 * h * h_
    return x1, y1, x2, y2

def single(f, out_path):
    print(f)
    img = cv2.imread(f)
    h, w, channels = img.shape
#    print(h, w, channels)
    f = f.replace("images", "yolo_txt")
    f_yolo = f.replace(".jpg", ".txt")
#    print('f_yolo:{}'.format(f_yolo))
    with open(f_yolo, 'r') as f:
        lines = f.readlines()
#        print(lines)

    # Write retcangle txt 
    basename = get_basename(f_yolo)
#    print(f_name)
    retangle_file = os.path.join(out_path, basename)
    print(retangle_file)
    file = open(retangle_file,'w')
    for line in lines:
        temp = line.split()
        label = classes[int(temp[0])]
        # ['1', , '0.43906', '0.52083', '0.34687', '0.15']
        x1, y1, x2, y2 = yolo_to_retangle(temp, w, h)
        x1, y1, x2, y2 = int(x1), int(x2), int(y2), int(y2)
        print('{} {:.6f} {} {} {}'.format(label, x1, y1, x2, y2))
        file.write('{} {:.6f} {} {} {}\n'.format(label, x1, y1, x2, y2))

#        #画图验证,注意画图坐标要转换成int格式
#        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0))
    file.close()
#    print('write to retange.txt')


if __name__ == '__main__':
    imgPath = './dog_cat_monkey/data/images'
    output_dir = './dog_cat_monkey/data/rectangle_txt'
    created_directory(output_dir)


# =============================================================================
#     # single process
# =============================================================================
#    f = './dog_cat_monkey/data/images/cats_016.jpg'
#    if isfile(f):
#        results = single(f, output_dir)

# =============================================================================
# #    # multiple
# =============================================================================
    for f in glob.glob(os.path.join(imgPath, "*.jpg")):
        single(f, output_dir)
