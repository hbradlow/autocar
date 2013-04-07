from SimpleCV import *
import IPython
from homography import *

def thresh(image):
    #target = np.array([247,255,31])
    #target = np.array([146,105,30])
    #target = np.array([103,71,18])
    #target = np.array([112,28,18])
    #target = np.array([8.,78.,86.])
    #target = np.array([219,71,49])
    #target = np.array([252,146,151])
    #target = np.array([237,91,108])
    target = np.array([253,112,100])
    full = np.array([255,255,255])
    thresh = np.array([.15,.15,.15])

    lower = target - thresh*full
    upper = target + thresh*full
    return Image(cv2.inRange(image.getNumpy(),lower,upper))

def get_blob_s(image):
    blobs = image.findBlobs()
    return blobs

def get_blob(image):
    blobs = image.findBlobs()
    if blobs:
        blob = max(blobs,key=lambda b: b._mHeight*b._mWidth)
        return (blob.x,blob.y)
    return None

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
    i_binary = thresh(i)
    blob = get_blob(i_binary)
    i_binary.show()
    IPython.embed()

    circlelayer = DrawingLayer((i.width, i.height))
    circlelayer.circle(blob, 10)
    i.addDrawingLayer(circlelayer)
    i.applyLayers()
    d = i.show()
    Q = get_homography(i_binary)
    check_points(d,Q)
    IPython.embed()
