# -*- coding: utf-8 -*-
"""
Created on Sun May  2 11:27:37 2021

@author: Thibaut
"""


# make a prediction for a new image.
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

# load and prepare the image


def load_image():
    # load the image
    # root = tk.Tk()
    # root.withdraw()

    # filename = filedialog.askopenfilenames()
    filename = "E:\\cat.jpg"

    img = load_img(filename, target_size=(224, 224))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 3 channels
    img = img.reshape(1, 224, 224, 3)
    # center pixel data
    img = img.astype('float32')
    img = img - [123.68, 116.779, 103.939]
    return img

# load an image and predict the class


def run_example():

    # load the image
    img = load_image()
    # load model
    model = load_model('E:\\final_model.h5')
    # predict the class
    result = model.predict(img)
    print("---------------")
    print("result : ", result)
    print("---------------")


# entry point, run the example
run_example()
