# FlyTracking
This project trained a model based on YOLOv5 and DeepSORT and built an interface for fly tracking in experimental videos. Our model can stably identify different fruit flies even in the low-fps videos. It's suitable for fruit fly courtship analysis, as well as other animals behavior videos.

## Requirements
    python==3.8
    PyQt5
    matplotlib>=3.2.2
    numpy>=1.18.5
    opencv-python>=4.1.2
    Pillow
    PyYAML>=5.3.1
    scipy>=1.4.1
    torch>=1.7.0
    torchvision>=0.8.1
    tqdm>=4.41.
    seaborn>=0.11.0
    pandas
    easydict
    

## Run
Use the following command to run our interface:

    python API/main.py

## Make your own datasets
Click the "label" button to make your own datasets using LabelImg.

## Train models
Click the "train" button to train your model based on your dataset. Before training, you should modify the parameters in the file:

    API/yolov5/config/train_config.yaml
    
Then, put your datasets (images and annotation) in corresponding foldes:

    API/yolov5/data
    
To make parameters suitable for your model, you can try different combinations and evaluate the performance of models. Plus, metrics of model's performance, such as precision and recall, can be found in:

    API/yolov5/runs/train


## Evaluate models
Click the  "evaluate" button to evaluate your model after training. The parameters about evaluation can be found in the file:

    API/yolov5/config/detect_config.yaml
    
The ouputs are images with detection boxes, which can be found in:
    
    API/yolov5/runs/detect
