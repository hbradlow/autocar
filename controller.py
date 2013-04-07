from vision.test2 import *
from imageextractor import get_image
from SimpleCV import *
import urllib
import time

debug = True

class Controller:
    def __init__(self):
        self.width = 500
        self.height = 500

    def process_image(self,image):
        self.width = image.width
        self.height = image.height

        i_binary = thresh(image)
        blob = get_blob(i_binary)
        self.blob = blob
        return blob

    def go_to(self):
        if self.blob:
            half = self.width/2.0
            left = self.blob[0]<half
            percent = float(self.blob[1])/self.height

            distance = 1-percent #TODO tune this
            print "GOTO: ",left,distance

            self.control(left,distance)

    def control(self,left,distance):
        return
        url = "https://agent.electricimp.com/Ywn0OQCdQZd6"

        direction = "/right"
        if left:
            direction = "/left"

        urllib.urlopen(url + direction)

        method = "/forward"
        urllib.urlopen(url + method)

        urllib.urlopen(url + direction)

frame_rate = 3

def get_blobs():
    c = Controller()
    im = Image(get_image())
    blob = c.process_image(im)
    return blob

if __name__=="__main__":
    while True:
        c = Controller()
        im = Image(get_image())
        blob = c.process_image(im)
        c.go_to()
        if debug and blob:
            circlelayer = DrawingLayer((im.width, im.height))
            circlelayer.circle(blob, 10)
            im.addDrawingLayer(circlelayer)
            im.applyLayers()
            d = im.show()
        time.sleep(1.0/frame_rate)
