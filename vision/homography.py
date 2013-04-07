from SimpleCV import *
from numpy import *
from numpy.linalg import *
#from IK import *
import time

HEIGHT = 9.025 #in cm
LENGTH = 5.160 #in cm
GPTS = [(0,0), (0,HEIGHT), (LENGTH,HEIGHT), (LENGTH,0)]

#compute image Homography, ipts is a list of 4 image coords of corners
#ipts should be list of tuples [(),(),(),()]
def compute_H(ipts):
	global GPTS

	print ipts
	x0 = GPTS[0][0]
	y0 = GPTS[0][1]
	x1 = GPTS[1][0]
	y1 = GPTS[1][1]
	x2 = GPTS[2][0]
	y2 = GPTS[2][1]
	x3 = GPTS[3][0]
	y3 = GPTS[3][1]

	u0 = ipts[0][0]
	v0 = ipts[0][1]
	u1 = ipts[1][0]
	v1 = ipts[1][1]
	u2 = ipts[2][0]
	v2 = ipts[2][1]
	u3 = ipts[3][0]
	v3 = ipts[3][1]

	A = array([[x0,y0,1,0,0,0,-u0*x0, -u0*y0], [0,0,0,x0,y0,1,-v0*x0,-v0*y0], [x1,y1,1,0,0,0,-u1*x1,-u1*y1], [0,0,0,x1,y1,1,-v1*x1,-v1*y1], [x2,y2,1,0,0,0,-u2*x2,-u2*y2], [0,0,0,x2,y2,1,-v2*x2,-v2*y2], [x3,y3,1,0,0,0,-u3*x3,-u3*y3], [0,0,0,x3,y3,1,-v3*x3,-v3*y3]])
	b = array([[u0],[v0],[u1],[v1],[u2],[v2],[u3],[v3]])

	x = solve(A,b)

	h11 = x[0]
	h12 = x[1]
	h13 = x[2]
	h21 = x[3]
	h22 = x[4]
	h23 = x[5]
	h31 = x[6]
	h32 = x[7]

	H = array([[h11,h12,h13], [h21,h22,h23], [h31,h32, 1]])
	return H

def get_corners(disp):
	corners = []
	while(disp.isNotDone()):
		time.sleep(0.001)
		up = disp.leftButtonUpPosition()
		if(len(corners)>=4):
			disp.quit()
			break
			return corners

		if(up):
			corners.append(up)
	return corners

def check_points(disp, Q):
	while(disp.isNotDone()):
		time.sleep(0.001)
		up = disp.leftButtonUpPosition()
		if up:
			print image_to_real(up, Q)

def real_to_image(coord, H):
	x = coord[0]
	y = coord[1]
	if H.all():
		u = (H[0][0]*x + H[0][1]*y + H[0][2])/(H[2][0]*x + H[2][1]*y + 1)
		v = (H[1][0]*x + H[1][1]*y + H[1][2])/(H[2][0]*x + H[2][1]*y + 1)
	return (u,v)

def image_to_real(coord, Q):
	u = coord[0]
	v = coord[1]
	if Q.all():
		x = (Q[0][0]*u + Q[0][1]*v + Q[0][2])/(Q[2][0]*u + Q[2][1]*v + Q[2][2])
		y = (Q[1][0]*u + Q[1][1]*v + Q[1][2])/(Q[2][0]*u + Q[2][1]*v + Q[2][2])
	return (x,y)

def main():
	im = Image("test.jpg")
	disp = im.show()
	corners = get_corners(disp)
	H = compute_H(corners)
	Q = inv(H)
	d = im.show()
	check_points(d, Q)

if __name__=="__main__":
    main()
