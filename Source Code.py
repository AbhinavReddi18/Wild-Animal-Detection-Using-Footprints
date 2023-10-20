# -*- coding: utf-8 -*-
"""Copy of mintu.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15uDppxu9haInzwR66UXF6wl7ICD4b7Iy
"""

ssimport tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.models import Model, Sequential
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, Flatten
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Flatten


# Step 1: Data Collection and Preprocessing
train_data_dir = '/content/drive/MyDrive/miniproject/dataset'
validation_data_dir = '/content/drive/MyDrive/miniproject/dataset'
test_data_dir = '/content/drive/MyDrive/miniproject/dataset'

datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

batch_size = 32

train_generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical'
)

validation_generator = datagen.flow_from_directory(
    validation_data_dir,
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical'
)

# Step 2: Data Splitting
# Split your dataset into training, validation, and test sets as needed.

# Step 3: Feature Extraction
base_model = ResNet50(weights='imagenet', include_top=False)
x = base_model.output
x = GlobalAveragePooling2D()(x)

# Create a model for feature extraction
feature_extraction_model = Model(inputs=base_model.input, outputs=x)

# Step 4: Probabilistic Neural Network (PNN)
pnn_model = Sequential()

# Add the feature extraction model
pnn_model.add(feature_extraction_model)

# Add a Flatten layer at the end
pnn_model.add(Flatten())

pnn_model.add(Dense(256, activation='relu'))
classes = list(train_generator.class_indices.keys())
pnn_model.add(Dense(len(classes), activation='softmax'))

# Compile the model
pnn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 5: Training
epochs = 100
history = pnn_model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=len(validation_generator)
)

# Step 6: Evaluation
test_generator = datagen.flow_from_directory(
    test_data_dir,
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

from google.colab import drive
drive.mount('/content/drive')



test_loss, test_accuracy = pnn_model.evaluate(test_generator)
print(f'Test Loss: {test_loss}')
print(f'Test Accuracy: {test_accuracy}')

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'])
plt.plot(history.history['loss'])
plt.xlabel('Time')
plt.legend(['accuracy', 'loss'])
plt.show()

classes

from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
def predict_image(image_path):
    img = load_img(image_path, target_size=(224,224,3))
    plt.imshow(img)
    plt.show()
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    pred = pnn_model.predict(images, batch_size=32)
    print("Actual: "+(image_path.split("/")[-1]).split("_")[0])
    print("Predicted: "+classes[np.argmax(pred)])

import cv2
image='/content/drive/MyDrive/miniproject/dataset/bear/Copy of bear-footprints-in-dirt0_jpg.rf.4e1c1ba6cd97ab0673bcc0428702c8ff.jpg'
predict_image(image)
# predictions = pnn_model.predict(img)
# print(predictions)



"""# New Section"""

