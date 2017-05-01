#coding:utf8
import cv2
import numpy as np


def double2uint8(I, ratio=1.0):
    return np.clip(np.round(I*ratio), 0, 255).astype(np.uint8)

def make_kernel(f):
    kernel = np.zeros((2*f+1, 2*f+1))
    for d in range(1, f+1):
        kernel[f-d:f+d+1, f-d:f+d+1] += (1.0/((2*d+1)**2))
    return kernel/kernel.sum()

def NLmeansfilter(I, h_=10, templateWindowSize=5,  searchWindowSize=11):
    f = templateWindowSize/2
    t = searchWindowSize/2
    height, width = I.shape[:2]
    padLength = t+f
    I2 = np.pad(I, padLength, 'symmetric')
    kernel = make_kernel(f)
    h = (h_**2)
    I_ = I2[padLength-f:padLength+f+height, padLength-f:padLength+f+width]

    average = np.zeros(I.shape)
    sweight = np.zeros(I.shape)
    wmax =  np.zeros(I.shape)
    for i in range(-t, t+1):
        for j in range(-t, t+1):
            if i==0 and j==0:
                continue
            I2_ = I2[padLength+i-f:padLength+i+f+height, padLength+j-f:padLength+j+f+width]
            w = np.exp(-cv2.filter2D((I2_ - I_)**2, -1, kernel)/h)[f:f+height, f:f+width]
            sweight += w
            wmax = np.maximum(wmax, w)
            average += (w*I2_[f:f+height, f:f+width])
    return (average+wmax*I)/(sweight+wmax)


I = cv2.imread('gaosi.jpg', 0)
sigma = 20.0
I1 = double2uint8(I + np.random.randn(*I.shape) *sigma)
R1 = double2uint8(NLmeansfilter(I1.astype(np.float), sigma, 5, 11))


cv2.imshow("R1", R1)
cv2.waitKey(10000)