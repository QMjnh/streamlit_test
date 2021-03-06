# -*- coding: utf-8 -*-


#@title Libraries
import tensorflow as tf
import tensorflow_hub as hub

import tensorflow_datasets as tfds

import time

from PIL import Image
import requests
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np

import os
import pathlib

#@title Gradio
#!pip install gradio --quiet
import gradio as gr

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.preprocessing import image
import tensorflow as tf

#@title Use TensorFlow Datasets to load oxford_flowers102 dataset
import tensorflow_datasets as tfds

(train, val, test), info = tfds.load('oxford_flowers102', 
                                      split=['train', 'validation', 'test'],
                                      shuffle_files=True,
                                      as_supervised=True, 
                                      with_info=True)
NUM_CLASSES = 102

#@title Save a text file list of flowers name
f = open("flower_names.txt", "w")
f.write(info.features['label'].names[0])

i=1
while i<102:
  f.write(" \n")
  f.write(info.features['label'].names[i])
  i+=1
f.close()

from google.colab import drive
drive.mount('/content/drive')

"""# Data_Preprocessing

"""

from tensorflow import cast, float32
from tensorflow.data.experimental import AUTOTUNE
from tensorflow import one_hot 
from tensorflow.image import resize

def preprocess_data(image, label):
  """
  Normalizes images: `uint8` -> `float32`.
  One hot encoding labels
  Resize to (224, 224)
  """


  return resize(cast(image, float32)/255. , [224, 224]), one_hot(label, 102)

"""# LOAD MODEL"""

# Load a previously trained model for gradio demonstration

#model2=tf.keras.models.load_model('your link here')

model2=tf.keras.models.load_model('/content/drive/MyDrive/Colab Notebooks/BiT fine_grained-17Jun-20220617T065450Z-001/BiT fine_grained-17Jun')


# model can be found here: https://drive.google.com/drive/folders/1R0-BCJynx_AUqFgNGB7LQzY1FqVXqHr0?usp=sharing

model2.summary()

"""# GRADIO"""

with open('/content/flower_names.txt') as f:
    labels = f.readlines()

from numpy import exp
def softmax(vector):
 e = exp(vector)
 return e / e.sum()

def image_to_output (input_img):

 


  gr_img=[]
  gr_img.append(input_img)
  img2=resize(cast(gr_img, float32)/255. , [224, 224])

  #print(img2)

  x_test=np.asarray(img2)

  prediction = model2.predict(x_test,batch_size=1).flatten()
  prediction=softmax(prediction)

  confidences = {labels[i]: float(prediction[i]) for i in range(102)}
#  confidences = {labels[i]:float(top[i]) for i in range(num_predictions)}

  return confidences

import gradio as gr

UI=gr.Interface(fn=image_to_output, 
             inputs=gr.inputs.Image(shape=(224,224)),
             outputs=gr.outputs.Label(num_top_classes=5),
             interpretation="default"
             )

"""# LAUNCH USER INTERFACE

**Voil??, the User Interface was built.**

 Run the cell below to interact with the model or you can also use the URL created below so your friends can use it too ;)

Text file containg names of flowers you can use to try out the model [here](https://drive.google.com/file/d/1dV97XD7I97KWqwml5b5qAMTHMJemew6A/view?usp=sharing)
"""

UI.launch()
