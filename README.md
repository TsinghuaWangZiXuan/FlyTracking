# FlyTracking
This project trained a model based on YOLOv5 and DeepSORT and built an interface for fly tracking in experimental videos. Our model can stably identify different fruit flies even in the low-fps videos. It's suitable for fruit fly courtship analysis, as well as other animals behavior videos.

## Requirement


## Run
Use the following command to run our interface:

    python main.py

## Make your own datasets
Click the "label" button to make your own datasets using LabelImg.

## Train the model
Click the "train" button to train your model based on your dataset. Before trainning, you should modify the parameters in the file:

    API/yolov5/config/train_config.yaml
    
To make parameters suitabel for your model, you can try different combinations and evaluate the performance of models.
