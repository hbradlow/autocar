from vision.test2 import *


class Controller:
    def __init__(self):
        self.width = 500
        self.height = 500

    def process_image(image):
        self.width = image.width
        self.height = image.height

        i_binary = thresh(i)
        blob = get_blob(i_binary)
        return blob

    def go_to(blob):
        half = self.width/2.0
        left = blob[0]<half
        percent = blob[1]/self.height

        distance = percent #TODO tune this

        control(left,distance)

    def control(left,distance):
        pass
