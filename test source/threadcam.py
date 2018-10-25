import cv2
from thread import start_new_thread as newthread
import capture
camName="e-con's 8MP Camera: e-con's 8MP"
def init():
	global x
	x=True
	global cam
	status,devNum,devName=capture.getCam(camName)
	if status !=False:
		cam=cv2.VideoCapture(int(devNum))
		devName
		newthread(save,())
	else:
		return "Camera not Connected"

def save():
	# cv2.imwrite("test"+str(i)+".png",im)
	y=True
	global x
	while True:
		# print "x "+str(x)
		if y==x:
			s,im=cam.read()
			# pass
		else:
			print "capping"
			x=not(x)
			cv2.imwrite("test.png",im)
# while True:
	# i=i+1
	# c=raw_input("Press any key to capture")
	# r=cam.grab()
	# if r:
		# r,im=cam.retrieve		
# init()
# while True:
# 	cap=raw_input("enter any key for capoturing")
# 	x=False
# # save()
