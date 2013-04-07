from SimpleCV import *
import numpy as np

class Tag:
    def __init__(self,position,histogram):
        self.position = position
        self.histogram = histogram

class Tagger:
    def __init__(self):
        self.tags = {}
        self.histogram_size = 10
    def process_blob(self,img,blob,s=50):
        (red, green, blue) = img.splitChannels(False)
        data = red.getNumpy()[:,:,0]
        x,y = blob
        b = data[x-s:x+s,y-s:y+s]

        i = Image(b)
        red_histogram = i.histogram(self.histogram_size)

    def update_tags(self,histogram):
        return
