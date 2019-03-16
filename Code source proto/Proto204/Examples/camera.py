
import picamera
import os
from PIL import Image

############################################################################
def take_picture():

    # Read image with opencv
  with picamera.PiCamera() as camera:
    camera.resolution = (1024, 720)
    camera.capture("f1.jpg")
    print("Picture f1.jpg taken")
    
############################################################################
if __name__ == "__main__":

	take_picture()
    
