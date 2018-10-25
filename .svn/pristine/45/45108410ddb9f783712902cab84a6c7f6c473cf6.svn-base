from imutils import contours
from skimage import measure
import numpy as np
import imutils
import cv2

threshold_pixel_value=35
dilate_no_iteration=2
minPix=30
image=cv2.imread('res.png')
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
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
	if labelMask[labels==label].shape[0]>minPix:
		
		mask=cv2.add(mask,labelMask)

# cv2.imwrite('int.png',mask)
cnts= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
cnts = contours.sort_contours(cnts)[0]
for (i, c) in enumerate(cnts):
	# draw the bright spot on the image
	(x, y, w, h) = cv2.boundingRect(c)
	((cX, cY), radius) = cv2.minEnclosingCircle(c)
	cv2.circle(image, (int(cX), int(cY)), int(radius),(0, 0, 255), 3)
	cv2.putText(image, "#{}".format(i + 1), (x, y - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
 
cv2.imwrite('int.png',image)
