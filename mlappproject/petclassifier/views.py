from queue import PriorityQueue
from django.shortcuts import render
from .models import mlModel

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

import tensorflow as tf
from tensorflow import  keras

import numpy as np



def home (request):
    petClassifierFiles= mlModel.objects.filter(priority=2)[0]
    pathArch=petClassifierFiles.architecture.path
    pathWeight= petClassifierFiles.weights.path
    
    with open(pathArch) as json_file:
        jsonConfig=json_file.read()
    
    model=tf.keras.models.model_from_json(jsonConfig)
    model.load_weights(pathWeight)
    caption=""
    if request.method =='POST':
        handle_uploaded_file(request.FILES['sentFile'])
        image= tf.keras.preprocessing.image.load_img('static/test1.jpg', target_size=(150,150,3))
        inputArr=tf.keras.preprocessing.image.img_to_array(image)
        inputArr=np.array([inputArr])
        pred=tf.keras.activations.sigmoid(model.predict(inputArr))[0][0]
        cat=1-pred
        caption=f'dog prob {pred}, cat prob{cat}'
    return render(request, 'home.html',{'caption':caption})

def handle_uploaded_file(f):
    with open('static/test1.jpg', 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
            
# Create your views here.
