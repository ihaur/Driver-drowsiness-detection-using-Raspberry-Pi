
import pytesseract
import picamera
from PIL import Image

############################################################################
def get_string(img_path):

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(img_path))
    return result
  

############################################################################
def read_picture():
    print ('--- Start recognize text from image ---')

    result1=get_string("im1.jpg")

    print (result1)
    

############################################################################
if __name__ == "__main__":

	read_picture()

