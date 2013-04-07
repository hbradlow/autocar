from SimpleCV import *
import IPython
from homography import *

def thresh(image):
    target = np.array([247,255,31])
    full = np.array([255,255,255])
    thresh = .3

    lower = target - thresh*full
    upper = target + thresh*full
    return Image(cv2.inRange(i.getNumpy(),lower,upper))

def get_blob(image):
    blobs = image.findBlobs()
    return (blobs[0].x,blobs[0].y)

def get_corners(input):
    blobs = input.findBlobs()
    corners = []
    for blob in blobs:
        corners.append((blob.x,blob.y))
    return corners

def get_homography(image):
    corners = get_corners(image)
    H = compute_H(corners)
    Q = inv(H)
    return Q

def find_goal(input):
    i = Image("test.jpg")
    i_binary = thresh(i)
    blob = get_blob(i_binary)
    return blob


if __name__=="__main__":
    i = Image("test2.jpg")
    IPython.embed()
    i_binary = thresh(i)
    blob = get_blob(i_binary)

    circlelayer = DrawingLayer((i.width, i.height))
    circlelayer.circle(blob, 10)
    i.addDrawingLayer(circlelayer)
    i.applyLayers()
    d = i.show()
    Q = get_homography(i_binary)
    check_points(d,Q)
    IPython.embed()
