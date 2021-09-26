import os
import random


def split_data():
    trainval_percent = 0.1
    train_percent = 0.9
    xmlfilepath = 'yolov5/data/images'
    txtsavepath = 'yolov5/data/ImageSets'

    total_xml = os.listdir(xmlfilepath)
    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    ftrainval = open('yolov5/data/ImageSets/trainval.txt', 'w')
    ftest = open('yolov5/data/ImageSets/test.txt', 'w')
    ftrain = open('yolov5/data/ImageSets/train.txt', 'w')
    fval = open('yolov5/data/ImageSets/val.txt', 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftest.write(name)
            else:
                fval.write(name)
        else:
            ftrain.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()

    sets = ['train', 'test', 'val']
    classes = ['fly']

    for image_set in sets:
        image_ids = open('yolov5/data/ImageSets/%s.txt' % image_set).read().strip().split()
        list_file = open('yolov5/data/%s.txt' % image_set, 'w')
        for image_id in image_ids:
            list_file.write('yolov5/data/images/%s.jpg\n' % image_id)
        list_file.close()
