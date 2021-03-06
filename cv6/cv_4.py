import cv2  as cv
import numpy as np

A = cv.imread('apple.jpg')
B = cv.imread('orange.jpg')
A = cv.resize(A,(1024,512))
B = cv.resize(B,(1024,512))
# generate Gaussian pyramid for A
G = A.copy()
gpA = [G]
for i in range(6):
	G = cv.pyrDown(G)
	gpA.append(G)

# generate Gaussian pyramid for B
G = B.copy()
gpB = [G]
for i in range(6):
	G = cv.pyrDown(G)
	gpB.append(G)

# generate Laplacian Pyramid for A
lpA = [gpA[5]]
for i in range(5,0,-1):
	GE = cv.pyrUp(gpA[i])
	L = cv.subtract(gpA[i-1],GE)
	lpA.append(L)

# generate Laplacian Pyramid for B
lpB = [gpB[5]]
for i in range(5,0,-1):
	GE = cv.pyrUp(gpB[i])
	L = cv.subtract(gpB[i-1],GE)
	lpB.append(L)
# Now add left and right halves of images in each level
#numpy.hstack(tup)
#Take a sequence of arrays and stack them horizontally
#to make a single array.
LS = []
for la,lb in zip(lpA,lpB):
	rows,cols,dpt = la.shape
	ls = np.hstack((la[:,0:cols//2], lb[:,cols//2:]))
	LS.append(ls)

# now reconstruct
ls_ = LS[0]
for i in range(1,6):
	ls_ = cv.pyrUp(ls_)
	ls_ = cv.add(ls_, LS[i])

# image with direct connecting each half
real = np.hstack((A[:,:cols//2],B[:,cols//2:]))

cv.imshow('Pyramid_blending2.jpg',ls_)
cv.imshow('Direct_blending.jpg',real)

cv.waitKey(0)