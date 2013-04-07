from PIL import Image
import numpy as np
import glumpy

from skimage import data, io, filter

import IPython

image = Image.open("test.jpg")

target = (247,255,31)
thresh = .3

print (np.asarray(image)[:,:,1]).shape
data = np.asarray(image)
R = np.asarray(image)[:,:,0]
R.flags.writeable = True
G = np.asarray(image)[:,:,1]
G.flags.writeable = True
B = np.asarray(image)[:,:,2]
B.flags.writeable = True
blank = np.zeros(data.shape,np.uint8)



i = 0

for (a,avalue),(b,bvalue),(c,cvalue) in zip(np.ndenumerate(R),np.ndenumerate(G),np.ndenumerate(B)):
    i = i+1
    if i%10000 == 0:
        print "-----------"
        print a,b,c
        print avalue,bvalue,cvalue
        print target[0]-thresh*255
        print target[0]+thresh*255

    a_good = avalue>target[0]-thresh*255 and avalue<target[0]+thresh*255
    b_good = bvalue>target[1]-thresh*255 and bvalue<target[1]+thresh*255
    c_good = cvalue>target[2]-thresh*255 and cvalue<target[2]+thresh*255
    if a_good and b_good and c_good:
        pass
    else:
        R[a] = 0
        G[b] = 0
        B[c] = 0

blank[:,:,0] = R
blank[:,:,1] = G
blank[:,:,2] = B

io.imshow(blank)
io.show()
