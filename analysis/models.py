from django.db import models
import cv2
from keras.applications.resnet import ResNet50, decode_predictions
import numpy as np
import os

# Create your models here.

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


# Create your models here.
class MyResNet50Model:

    def myImagePredict(self, imgName):
        md = ResNet50(weights='imagenet')
        img = cv2.imread(imgName)
        imgcv = cv2.resize(img, (224, 224))
        x = np.reshape(imgcv, (1, 224, 224, 3))
        preds = md.predict(x)

        print("*" * 30)
        print(decode_predictions(preds, top=5)[0])
        print("*" * 30)

        return decode_predictions(preds, top=5)[0]
