# FlyTracking
This project trained a model based on YOLOv5 and DeepSORT and built an interface for fly tracking in experimental videos. Our model can stably identify different fruit flies even in the low-fps videos. It's suitable for fruit fly courtship analysis, as well as other animals behavior videos.

<div align="left">
  
<img src="https://github.com/TsinghuaWangZiXuan/FlyTracking/blob/master/API/Tracker.png" height="300" width="400" >
  
</div>

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
Click "label" button to make your own datasets using LabelImg.

## Train models
Click "train" button to train your model based on your dataset. Before training, you should modify the parameters in the file:

    API/yolov5/config/train_config.yaml
    
Then, put your datasets (images and annotation) in corresponding folders:

    API/yolov5/data/
    
To make parameters suitable for your model, you can try different combinations and evaluate the performance of models. Plus, metrics of model's performance, such as precision and recall, can be found in:

    API/yolov5/runs/train/


## Evaluate models
Click "evaluate" button to evaluate your model after training. The parameters about evaluation can be found in the file:

    API/yolov5/config/detect_config.yaml
    
The ouputs are images with detection boxes, which can be found in:
    
    API/yolov5/runs/detect/
    
## Track
Click "track" button to process videos. The parameters of the tracker can be found in the file:

    API/deepsort/config/track_config.yaml
    
The outputs including video and text can be found in:

    API/deepsort/inference/output/

## References
```latex
@misc{yolov5deepsort2020,
    title={Real-time multi-object tracker using YOLOv5 and deep sort},
    author={Mikel Broström},
    howpublished = {\url{https://github.com/mikel-brostrom/Yolov5_DeepSort_Pytorch}},
    year={2020}
}
```
