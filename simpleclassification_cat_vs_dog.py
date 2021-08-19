# -*- coding: utf-8 -*-
"""Copy of Simpleclassification cat vs dog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XD8gc-8U0c6AbNjna0nKNwplrOCrgE4F

Simple classification algorithm

importing data from kaggle API
"""

import os
os.environ['KAGGLE_USERNAME'] = "anandyadav21" # username from the json file
os.environ['KAGGLE_KEY'] = "115a6f58571ea214070851195db83a5e" # Provide your key from the json file
!kaggle competitions download -c dogs-vs-cats # api copied from kaggle

"""Importing libraries"""

import zipfile
import random
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from shutil import copyfile

"""Exracting files"""

from zipfile import ZipFile

file_name = "/content/train.zip"

with ZipFile(file_name, 'r') as zip:
  zip.extractall()
  print('done')

"""checking no of images"""

data_dir_list = os.listdir('/content/train')
#print(data_dir_list)

path, dirs, files = next(os.walk("/content/train"))
file_count = len(files)
print(file_count)

"""Making folder cat and dogs"""

original_dataset_dir = '/content/train'
base_dir = '/content/cats_and_dogs_small'
os.mkdir(base_dir) #make base directory

"""making three folders test,validation and train"""

#Create directory paths

train_dir = os.path.join(base_dir, 'train')
os.mkdir(train_dir)

validation_dir = os.path.join(base_dir, 'validation')
os.mkdir(validation_dir)

test_dir = os.path.join(base_dir, 'test')
os.mkdir(test_dir)

train_cats_dir = os.path.join(train_dir, 'cats')
os.mkdir(train_cats_dir)

train_dogs_dir = os.path.join(train_dir, 'dogs')
os.mkdir(train_dogs_dir)

validation_cats_dir = os.path.join(validation_dir, 'cats')
os.mkdir(validation_cats_dir)

validation_dogs_dir = os.path.join(validation_dir, 'dogs')
os.mkdir(validation_dogs_dir)

test_cats_dir = os.path.join(test_dir, 'cats')
os.mkdir(test_cats_dir)

test_dogs_dir = os.path.join(test_dir, 'dogs')
os.mkdir(test_dogs_dir)

"""copying the images into the cat folder"""

import shutil

def createFName(org_data_dir, train_data_class_dir, rangeInput1, rangeInput2):
    "This funciton is to create the source and desitnation paths and copy the data."
    fnames = ['cat.{}.jpg'.format(i) for i in range(rangeInput1,rangeInput2)]
    for fname in fnames:
        src = os.path.join(org_data_dir, fname)
        dst = os.path.join(train_data_class_dir, fname)
        #print(src,dst)
        shutil.copyfile(src, dst)

createFName(original_dataset_dir,train_cats_dir,0,1000)
createFName(original_dataset_dir,validation_cats_dir,1000,1500)
createFName(original_dataset_dir,test_cats_dir,1500,2000)

"""copying images into the dog folder"""

def createFName(org_data_dir, train_data_class_dir, rangeInput1, rangeInput2):
    "This funciton is to create the source and desitnation paths and copy the data."
    fnames = ['dog.{}.jpg'.format(i) for i in range(rangeInput1,rangeInput2)]
    for fname in fnames:
        src = os.path.join(org_data_dir, fname)
        dst = os.path.join(train_data_class_dir, fname)
        #print(src,dst)
        shutil.copyfile(src, dst)


createFName(original_dataset_dir,train_dogs_dir,0,1000)
createFName(original_dataset_dir,validation_dogs_dir,1000,1500)
createFName(original_dataset_dir,test_dogs_dir,1500,2000)

"""reading no if images in folders"""

print('total training cat images:', len(os.listdir(train_cats_dir)))
print('total training dog images:', len(os.listdir(train_dogs_dir)))
print('total validation cat images:', len(os.listdir(validation_cats_dir)))

print('total validation dog images:', len(os.listdir(validation_dogs_dir)))
print('total test cat images:', len(os.listdir(test_cats_dir)))
print('total test dog images:', len(os.listdir(test_dogs_dir)))

"""compiling"""

from keras import layers
from keras import models

#Created sequential models using Keras
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.summary()
model.compile(optimizer=RMSprop(lr=0.001), loss='binary_crossentropy', metrics=['acc'])

"""preprocessing data using keras"""

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(150, 150), 
                                                    batch_size=20,
                                                    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(validation_dir,
                                                        target_size=(150, 150),
                                                        batch_size=20,
                                                        class_mode='binary')

"""fitting the model"""

history = model.fit_generator(train_generator,
                              steps_per_epoch=100,
                              epochs=30,
                              validation_data=validation_generator,
                              validation_steps=10)

"""training and validation results"""

model.save('cats_and_dogs_small_1.h5')

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()