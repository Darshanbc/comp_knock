#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
from PIL import Image
import os
from thread import start_new_thread as newthread
import time,threadcam

Disconnected_msg="*Camera not Connected"
camName="e-con's 8MP Camera: e-con's 8MP"

imName=""
anImgName=""
# cam=""
        

def analyse(path):
    print (str(path)+" isd the path of img")
    im = Image.open(path)
    px = im.load()
    (width, height) = im.size
    r = g = b = 0
    for x in range(width):
        for y in range(height):
            (tr, tg, tb) = im.getpixel((x, y))
            r = tr + r
            b = tb + b
            g = tg + g

    r = r / (width * height)
    g = g / (width * height)
    b = b / (width * height)
    lvl = [r, g, b]
    print(lvl)
    label = ['R', 'G', 'B']
    bar = plt.bar(label, lvl)
    bar[0].set_color('r')
    bar[1].set_color('g')
    bar[2].set_color('b')

    imName=str(int(time.time()*1000))
    plt.savefig(imName+'.png')
    return "./"+imName+'.png'

def statusUpdate():
    status,devNum,devName=getCam(camName) 
    if status:
        return devName
    else:
       
        return Disconnected_msg


def init():
    global x
    print("executing init")
    x=True
    global cam,Disconnected_msg
    isConnected,devNum,devName=getCam(camName)
    print (str(isConnected))
    if isConnected:
        cam=cv2.VideoCapture(int(devNum))
        cam.set(28, 67)
        #newthre9d(save,())
        return devName
    else:
        print (Disconnected_msg)
        return Disconnected_msg

def save():
    y=True
    global x
    global imName,anImgName

    while True:
        # print "x "+str(x)
        if y==x:
            s,im=cam.read()
            # pass
        else:
            # print "capping"
            newframe=im
            lvl= newframe.mean(axis=(0,1))
            print (newframe.max(axis=(0,1)))
            print (newframe)
            x=not(x)
            imName=str(int(time.time()*1000))
            cv2.imwrite(os.path.join(os.getcwd(),'static/images',imName+".png"),newframe)
            # plt.set_ylim(255)
            label = ['B', 'G', 'R']
            bar = plt.bar(label, lvl)
            bar[0].set_color('b')
            bar[1].set_color('g')
            bar[2].set_color('r')
            for a,b in zip(range(len(label)),lvl):
                plt.text(a,b,str(int(b)))

            anImgName=str(int(time.time()*1000))
            plt.savefig(os.path.join(os.getcwd(),'static/images',anImgName+'.png'))
            plt.close()
            print ("capturing image")

            
def capture():
    global x
    x=False
    time.sleep(1)
    global imName,anImgName
    if imName!="" and statusUpdate()!=Disconnected_msg:
        imPath="./images/"+imName+".png"
        imName=""
        anImgPath="./images/"+anImgName+".png"
        anImgName=""
        return True,imPath,anImgPath    # return True,"./test.png"
    else:
        return False, None,None 

def getCam(camName):
    devList=os.listdir('/sys/class/video4linux/')
    for dev in devList:
        f=open(os.path.join('/sys/class/video4linux',dev,'name'),'r')
        newCam=f.read()
        if newCam.find(camName)!=-1:
            return True, int(filter(str.isdigit,dev)),camName
    return False ,None, None
