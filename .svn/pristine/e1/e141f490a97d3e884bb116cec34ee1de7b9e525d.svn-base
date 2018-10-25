import cv2,capture
from thread import start_new_thread as newthread
import numpy as np 
from imutils import contours
from skimage import measure
import imutils
capture.init()

cam=capture.cam
threshold_pixel_value=35
dilate_no_iteration=5
minPix=30
knock_off=False
def read():
	global im
	while True:
		im=cam.read()

newthread(read,())

imqueue=[]

while True:
	inp=raw_input("Enter r for capture c for compare ")
	# print inp
	# print "  "
	# print type(inp)
	# print inp=='r'
	if inp=='r':
			NewFrame=im
			imqueue.append(NewFrame[1])
	elif inp=='c':
		if len(imqueue)==2:
			cv2.imwrite('org.png',imqueue[0])
			cv2.imwrite('org1.png',imqueue[1])
			res=np.zeros(imqueue[0].shape,dtype='uint8')
			for index in np.ndindex(imqueue[0].shape):
				if imqueue[0][index]<imqueue[1][index]:
					continue
					# imqueue[1][index]-imqueue[0][index]
				else:
					res[index]= imqueue[0][index]-imqueue[1][index]

			# cv2.imwrite('res.png',res)
			# enobj=mark.encircle()
			# print res.shape
			# enobj.mark(imqueue[1],res)
# ---------------------
			cv2.imwrite('res.png',res)
			gray=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
			blurred=cv2.GaussianBlur(gray,(5,5),0)
			thresh = cv2.threshold(blurred, threshold_pixel_value, 255, cv2.THRESH_BINARY)[1]
			thresh=cv2.dilate(thresh,None,dilate_no_iteration)
			labels=measure.label(thresh,neighbors=8,background=0)
			mask=np.zeros(thresh.shape,dtype='uint8')
			for label in np.unique(labels):
				if label==0:
					continue
				labelMask=np.zeros(thresh.shape,dtype='uint8')
				labelMask[labels==label]=255
				# global 
				numPix=labelMask[labels==label].shape[0]
				print numPix
				if numPix>minPix:
					knock_off=True
					mask=cv2.add(mask,labelMask)

			# cv2.imwrite('int.png',mask)
			print 'knock_off '+str(knock_off)
			if knock_off:
				cnts= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
				cnts = cnts[0] if imutils.is_cv2() else cnts[1]
				# cnts = contours.sort_contours(cnts)[0]
				for (i, c) in enumerate(cnts):
					# draw the bright spot on the image
					(x, y, w, h) = cv2.boundingRect(c)
					((cX, cY), radius) = cv2.minEnclosingCircle(c)
					cv2.circle(imqueue[1], (int(cX), int(cY)), int(radius),(0, 0, 255), 3)
					cv2.putText(imqueue[1], "#{}".format(i + 1), (x, y - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
				cv2.imwrite('marked.png',imqueue[1])
				 
			# cv2.imwrite('ORG1.png',imqueue[1])

# --------------------


			# cv2.imwrite('org.png',imqueue[0])
			imqueue=[]

		else:
			print "insufficient input"
	else:
		print"improper input"



