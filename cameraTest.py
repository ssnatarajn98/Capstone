from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.start_preview()
cnt =  0
while(1):
    cnt = cnt + 1
    sleep(.2)
    camera.capture('/home/pi/Desktop/ImageTestFolder/imageTest%s.jpg' % cnt)
camera.stop_preview()