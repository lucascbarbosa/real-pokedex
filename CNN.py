import cv2 as cv
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras import layers
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
import os
plt.style.use('fivethirtyeight')

images_path = 'C:/Users/lucas/Documents/GitHub/Pokedex/Pokemon Pictures'
pokemons = os.listdir(images_path)
num_pokemons = 151
classes = np.identity(num_pokemons)
train = []
test = []
for i in range(num_pokemons):
    pokemon = pokemons[i]
    try:
        pokeimgs = os.listdir('/'.join([images_path,pokemon])+'/')
    
        for j in range(1,11):
            img = pokeimgs[j]
            imgdata = cv.imread('/'.join([images_path,pokemon,img]))
            if j <= 7:
                train.append(imgdata)
            else:
                test.append(imgdata)
    except:
        pass

train = np.array(train).reshape()

print(len(train))
print(len(test))
        