from SimpleCV import *
import IPython

target = np.array([247,255,31])
full = np.array([255,255,255])
thresh = .3

lower = target - thresh*full
upper = target + thresh*full
i = Image("test.jpg")
a = cv2.inRange(i.getNumpy(),lower,upper)
filtered = Image(a)
IPython.embed()
