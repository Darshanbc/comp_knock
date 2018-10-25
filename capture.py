#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
from PIL import Image
import os
from thread import start_new_thread as newthread, allocate_lock
import time
import analyse
import cryptoOps
import dbops
import copy
Disconnected_msg = "*Camera not Connected"
camName = "e-con's 8MP Camera: e-con's 8MP"
DMC = 'H78HSR5JNNQSUIY'
lineNo = 12
stationNo = 3
PCBA_family = "103.78.7782"
imageInsertOp = "insert_image"
imName = ""
anImgName = ""
lock=allocate_lock()
curFrame=None
cam=None

def statusUpdate():
    status, devNum, devName = getCam(camName)
    if status:
        return devName
    else:
        return Disconnected_msg


def isConnected():
    status, devNum, devName = getCam(camName)
    return status


def init():
    global cam, Disconnected_msg
    isConnected, devNum, devName = getCam(camName)


    print("executing init")
    if not(isConnected):
        return Disconnected_msg
    elif isConnected and cam==None:
        cam = cv2.VideoCapture(int(devNum))
        print "cam opened status"+str(cam.isOpened())
        if not(cam.isOpened()):
            return "Error Initializing Camera"
        else:
            newthread(continuos_cap, ())
            return devName
    elif not(cam.isOpened()):
        cam = cv2.VideoCapture(int(devNum))
        print "cam opened status" + str(cam.isOpened())
        if not (cam.isOpened()):
            return "Error Initializing Camera"
        else:
            newthread(continuos_cap, ())
            return devName
    elif cam.isOpened():
        return camName



def continuos_cap():
    global cam,curFrame,curStatus
    while True:
        # lock.acquire()
        if cam.isOpened()and cam!=None:
            curStatus,curFrame = cam.read()
        # lock.release()
def captureAnalyse(user):
    frameData=[]
    if not(cam.isOpened()):
        return False, None, None
    lock.acquire()
    cv2.waitKey(2)
    frameData.append(copy.deepcopy(curStatus))
    frameData.append(copy.deepcopy(curFrame))
    lock.release()
    dbObj = dbops.dbConn()
    dbObj.operation('login')
    print "collection =" + str(dbObj.get_collection())
    if len(frameData)!=0 and frameData[0]:
        newframe = frameData[1]
        print newframe
        imName = str(int(time.time() * 1000))
        cv2.imwrite(os.path.join(os.getcwd(), 'static/images', imName + ".png"), newframe)
        imPath = "./images/" + imName + ".png"
        anImgPath = None
        # encrypt image
        encryptobj = cryptoOps.CryptoOps()
        # keyObj = dbops.dbConn()
        # key = keyObj.getKey(user)
        key = str(next(dbObj.query({'empid': "admin"}, {"key": 1}),None)['key'])

        cipher_text = encryptobj.encrypt(newframe, key)

        # insert image
        dbObj = dbops.dbConn()
        dbObj.operation('insert_image')
        print "insert image collection ="+str(dbObj.get_collection())
        attr = {}

        attr['image'] = cipher_text
        attr['user'] = user
        attr['DMC'] = DMC
        attr['PCBA family'] = PCBA_family
        if user != 'admin':

            attr['line No.'] = lineNo
            attr['station'] = stationNo

            anImgMatrix = analyse.Analyse(PCBA_family, newframe,key)
            anImgName = str(int(time.time() * 1000))
            AbsAnImgPath=os.path.join(os.getcwd(), 'static/images', anImgName + ".png")
            cv2.imwrite(AbsAnImgPath, anImgMatrix)
            anImgPath='./images/'+anImgName+'.png'
            cipher_text = encryptobj.encrypt(anImgMatrix, key)
            attr["analysedImage"] = cipher_text
            dbObj.insert(attr)

        elif user == 'admin':
            # attr['PCBA family']=PCBA_family
            dbObj.insert(attr)

        return frameData[0], imPath, anImgPath  # return True,"./test.png"
    else:
        return frameData[0], None, None



def getCam(camName):
    devList = os.listdir('/sys/class/video4linux/')
    for dev in devList:
        f = open(os.path.join('/sys/class/video4linux', dev, 'name'), 'r')
        newCam = f.read()
        if newCam.find(camName) != -1:
            return True, int(filter(str.isdigit, dev)), camName
    return False, None, None
