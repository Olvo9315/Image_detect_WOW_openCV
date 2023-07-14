import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('p.png',0)          # queryImage
img2 = cv2.imread('capt1.png',0) # trainImage

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)
