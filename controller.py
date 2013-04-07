from vision.test2 import *
from imageextractor import get_image
from SimpleCV import *
import urllib2
import time

debug = True

frame_rate = 1.5

class Controller:
    def __init__(self):
        self.width = 500
        self.height = 500
        self.lefts = []
        self.distances = []
        self.distance = None
        self.down_counter = 0

        url = "https://agent.electricimp.com/Ywn0OQCdQZd6"
        try:
            urllib2.urlopen(url + "/straight",timeout=.1)
        except:
            pass

    def is_high(self):
        if self.distance:
            return self.down_counter<3
        return True

    def process_image_blobs(self,image):
        self.width = image.width
        self.height = image.height

        i_binary = thresh(image)
        blobs = get_blob_s(i_binary)
        return blobs

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
            if abs((self.blob[0]-half)/half)<.05:
                left = -1
            percent = float(self.blob[1])/self.height

            distance = 1-percent #TODO tune this
            self.distance = distance
            if self.distance:
                if self.distance<.09:
                    self.down_counter += 1
            print "GOTO: ",left,distance

            self.control(left,distance)
    def go_back(self):
        for left,distance in reversed(zip(self.lefts,self.distances)):
            self.control(left,distance,back=True)
    def control(self,left,distance,back=False):
        self.lefts.append(left)
        self.distances.append(distance)
        url = "https://agent.electricimp.com/Ywn0OQCdQZd6"
        to = .1

        if left != -1:
            print "STRAIGHT"
            direction = "/right"
            if left:
                direction = "/left"

            try:
                urllib2.urlopen(url + direction,timeout=to)
            except:
                pass

            time.sleep(.5/frame_rate)

        method = "/forward"
        if back:
            method = "/back"
        method += str(distance*1.5)
        try:
            urllib2.urlopen(url + method,timeout=to)
        except:
            pass

        time.sleep(.5/frame_rate)

        try:
            urllib2.urlopen(url + "/straight",timeout=to)
        except:
            pass


def process_blob(img,blob,s=50):
    (red, green, blue) = img.splitChannels(False)
    data = red.getNumpy()[:,:,0]
    x,y = blob
    b = data[x-s:x+s,y-s:y+s]

    i = Image(b)
    red_histogram = i.histogram(10)
    print red_histogram

def get_blobs():
    c = Controller()
    im = Image(get_image())
    blobs = c.process_image_blobs(im)
    r = [[b.x,b.y] for b in blobs]
    return r

def get_blobs2():
    c = Controller()
    im = Image(get_image())
    blobs = c.process_image_blobs(im)
    im.show()
    if blobs:
        r = [[b.x,b.y] for b in blobs]
        for blob in r:
            process_blob(im,blob)
        return r
    return  None


if __name__=="__main__":
    c = Controller()
    while c.is_high():
        im = Image(get_image())
        blob = c.process_image(im)
        if blob:
            c.go_to()
            print c.distance
        else:
            print "Cant see it"
        if debug and blob:
            circlelayer = DrawingLayer((im.width, im.height))
            circlelayer.circle(blob, 10)
            im.addDrawingLayer(circlelayer)
            im.applyLayers()
            d = im.show()
    c.go_back()
