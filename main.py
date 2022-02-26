import pyautogui as pag
import keyboard
from PIL import ImageGrab, ImageOps, Image
import numpy as np
import pickle

trex_square = (120, 280, 420, 460)
restart_square = (450, 380, 490, 420)

def is_done():
    image = ImageGrab.grab(restart_square)
    image = ImageOps.grayscale(image)
    image = np.array(image)

    restart_image = np.load("restart.npy")
    norm =  np.linalg.norm((restart_image - image), ord=1)

    if norm < 100:
        return True
    else:
        return False

def get_data():
    pag.click(474, 400)
    images = []
    labels = []
    while len(images) < 1000 and not is_done():
        image = ImageGrab.grab(trex_square)
        image = ImageOps.grayscale(image)
        image = np.array(image)

        if keyboard.is_pressed("space"):
            label = 0
        elif keyboard.is_pressed("down"):
            label = 1
        else:
            label = 2
        
        images.append(image)
        labels.append(label)
    
    return images, labels


def save_data(images, labels):
    try:
        with open("images.pickle", "rb") as fr_image:
            image_data = pickle.load(fr_image)
        with open("labels.pickle", "rb") as fr_label:
            label_data = pickle.load(fr_label)
    except:
        with open('images.pickle', 'wb') as fw_image:
            pickle.dump(images, fw_image)
        with open('labels.pickle', 'wb') as fw_label:
            pickle.dump(labels, fw_label)
        return
    
    for i in range(len(images)):
        if images[i] in image_data:
            pass
        else:
            image_data.append(images[i])
            label_data.append(labels[i])
    
    with open('images.pickle', 'wb') as fw_image:
        pickle.dump(image_data, fw_image)
    with open('labels.pickle', 'wb') as fw_label:
        pickle.dump(label_data, fw_label)

def test_data():
    with open("images.pickle", "rb") as fr_image:
        image_data = pickle.load(fr_image)
    with open("labels.pickle", "rb") as fr_label:
        label_data = pickle.load(fr_label)
    
    cnt = 0
    
    pag.click(474, 400)
    while not is_done():
        image = ImageGrab.grab(trex_square)
        image = ImageOps.grayscale(image)
        image = np.array(image)

        norm_arr = [np.linalg.norm((data - image), ord=1) for data in image_data]
        idx = np.argmin(norm_arr)
        action = label_data[idx]
        
        if action == 0:
            pag.keyDown("space")
            pag.keyUp("space")
        elif action == 1:
            pag.keyDown("down")
            pag.keyUp("down")
        else:
            pass
        
        cnt += 1

    print("game done, cnt:", cnt)

def get_len():
    with open("images.pickle", "rb") as fr_image:
        image_data = pickle.load(fr_image)
    return len(image_data)

test_data()
