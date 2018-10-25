import cv2
from thread import start_new_thread as newthread
import numpy as np
from imutils import contours
from skimage import measure
import imutils
import cryptoOps
import dbops
threshold_pixel_value=35
dilate_no_iteration=5
minPix=30
knock_off=False
insertImage="insert_image"
login='login'

def Analyse(PCBA_family,anImgMatrix,key):
    refImage=getrefImage(PCBA_family)
    res = np.zeros(anImgMatrix.shape, dtype='uint8')
    for index in np.ndindex(anImgMatrix.shape):
        if refImage[index]<anImgMatrix[index]:
            continue
        else:
            res[index]=refImage[index]-anImgMatrix[index]

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, threshold_pixel_value, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, dilate_no_iteration)
    labels = measure.label(thresh, neighbors=8, background=0)
    mask = np.zeros(thresh.shape, dtype='uint8')
    for label in np.unique(labels):
        if label == 0:
            continue
        labelMask = np.zeros(thresh.shape, dtype='uint8')
        labelMask[labels == label] = 255
        # global
        numPix = labelMask[labels == label].shape[0]
        print numPix
        if numPix > minPix:
            knock_off = True
            mask = cv2.add(mask, labelMask)

    # cv2.imwrite('int.png',mask)
    print 'knock_off ' + str(knock_off)
    if knock_off:
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        # cnts = contours.sort_contours(cnts)[0]
        for (i, c) in enumerate(cnts):
            # draw the bright spot on the image
            (x, y, w, h) = cv2.boundingRect(c)
            ((cX, cY), radius) = cv2.minEnclosingCircle(c)
            cv2.circle(anImgMatrix, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
            cv2.putText(anImgMatrix, "#{}".format(i + 1), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    return anImgMatrix


def getrefImage(PCBA_family):
    querystring={"PCBA family":PCBA_family,"user":'admin'}
    projection={'image':1}
    dbobj=dbops.dbConn()
    dbobj.operation(insertImage)
    refImg=str(next(dbobj.query(querystring,projection))['image'])

    dbobj.operation(login)
    querystring={'empid':'admin'}
    projection={'key':1}
    key=str(next(dbobj.query(querystring,projection))['key'])

    cryObj=cryptoOps.CryptoOps()
    return cryObj.decrypt(key,refImg)

