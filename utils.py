import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import os
import time
import tqdm

def saliency_map(img):
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyMap) = saliency.computeSaliency(img)
    threshMap = cv2.threshold(saliencyMap.astype("uint8"), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imshow("Input", img)
    cv2.imshow("Output", saliencyMap)
    cv2.waitKey(0)
    return threshMap

def mosaic(img, n):
    w, h = img.size
    mosaic = [[0] * n] * n
    for i in tqdm.tqdm(range(n)):
        for j in range(n):
            count = 0
            avgs = [0, 0, 0]
            for x in range(int(i*(w/n)), int((i+1)*w/n)):
                for y in range(int(j*(h/n)), int((j+1)*(h/n))):
                    # img = Image.open('RubixMosaic/test.jpg')
                    a, b, c = img.getpixel((x, y))
                    avgs[0] += a
                    avgs[1] += b
                    avgs[2] += c
                    count += 1
            mosaic[i][j] = (avgs[0] / count, avgs[1] / count, avgs[2] / count)
    return mosaic

def get_closest_color(color, color_list):
    color_index = 0
    for i in range(len(color_list)):
        if get_distance(color, color_list[i]) < get_distance(color, color_list[color_index]):
            color_index = i
    return color_index

def get_distance(color1, color2):
    return np.sqrt((color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2)

