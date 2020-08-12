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

class Study:

    def __init__(self,x_train, y_train,x_test,y_test,test):
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.test = test
        self.num_pokemons = 721
        
    def load_dataset(self):
        images_path = 'C:/Users/lucas/Documents/GitHub/Pokedex/pokemon_jpg'
        pokemons = os.listdir(images_path+'/')
        imgs = len(pokemons)
        classes = []
        imgsdata = []
        for img in pokemons:
            imgdata = cv.imread(os.path.join(images_path,img))
            imgdata = cv.resize(imgdata, (32, 32),0,0,cv.INTER_LINEAR)
            imgsdata.append(imgdata)
            classes.append(int(img.split('.')[0].split('-')[0][:3]))
        imgsdata = np.array(imgsdata).reshape(819,32,32,3)
        classes_arr = np.zeros((len(classes),self.num_pokemons))
        for i in range(len(classes_arr)):
            classe_idx = classes[i]-1
            classes_arr[i][classe_idx] = 1
        num_test = int(imgs*self.test)
        num_train = imgs-num_test
        test_indexes = np.random.choice(classes_arr.shape[0], num_test, replace=False)  
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        for idx in test_indexes:
            self.x_test.append(imgsdata[idx])
            self.y_test.append(classes_arr[idx])

        self.x_test = np.array(self.x_test)/255.0
        self.y_test = np.array(self.y_test)
        self.x_train = np.delete(imgsdata, test_indexes,0)/255.0
        self.y_train = np.delete(classes_arr, test_indexes,0)

    def model(self):
        
        model = Sequential()
        model.add(Conv2D(3, (3, 3), activation='relu', input_shape=(32,32,3)))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(self.num_pokemons*100, activation = 'relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_pokemons * 50, activation = 'relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_pokemons * 25 , activation = 'relu'))
        model.add(Dense(self.num_pokemons, activation = 'softmax'))
        # specify the loss function and optimizer
        model.compile(loss= 'categorical_crossentropy',
         optimizer=tf.train.AdamOptimizer(0.001),
         metrics = ['accuracy'])
        self.hist = model.fit(self.x_train, self.y_train, batch_size = 32, epochs = 500, verbose=1, validation_split = 0.1)
    
        # save the model
        model.save('pokedex.model')

    def predict(self):
        pred = model.predict(self.x_test)
        index = 32 #the index you want to test
        result = np.argmax(pred[index])
        result_class = classes[result]
        print("Predicted index: %d" % np.argmax(pred[index]))
        print("Predicted should match label: %d" %(np.where(self.y_test[index]==1)[0]+1))
        plt.imshow(self.x_test[index], interpolation='nearest')


    def evaluate_model(self):
        model.evaluate(self.x_test, self.y_test)

    def plothist(self):
        plt.plot(self.hist.history['val_accuracy'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.show



if __name__ == "__main__":
    
    std = Study(None,None,None,None,0.3)
    std.load_dataset()
    std.model()