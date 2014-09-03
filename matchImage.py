#!/usr/bin/python
'''
# example
python matchFace.py -i /tmp/fox/manU2008.JPG -t /tmp/fox/JSPark.JPG -o /tmp/fox/Result.JPG
# for some linux enviroments
import matplotlib
matplotlib.use('TkAgg')

# matplotlib ( is a python 2D plotting library )
http://matplotlib.org/api/pyplot_api.html

# opencv (is an open source computer vision and machine learning software library.)
http://opencv.org/
# template matching
http://docs.opencv.org/doc/tutorials/imgproc/histograms/template_matching/template_matching.html#which-are-the-matching-methods-available-in-opencv

# NumPy (is the fundamental package for scientific computing with Python.)
http://www.numpy.org/
'''

import sys, getopt
import cv2
import numpy as np
from matplotlib import pyplot as plt
 
class compareImage:
	def __init__(self,pic,picTmp,picRst):
		# definite a variables
		self.pic = pic
                self.picTmp = picTmp
                self.picRst = picRst
                self.w = 0
		self.h = 0
 
	def compare(self):
		# read and compare a images.
		self.imgRGB = cv2.imread(self.pic)
		self.imgGray = cv2.cvtColor(self.imgRGB, cv2.COLOR_BGR2GRAY)
		imgTmp = cv2.imread(self.picTmp,0)
		self.w, self.h = imgTmp.shape[::-1]
		self.res = cv2.matchTemplate(self.imgGray,imgTmp, cv2.TM_CCOEFF_NORMED)
		threshold = np.amax(self.res) 
		self.loc = np.where( self.res >= threshold)
 
	def display(self):
		# Drawing rectangle on matching area.                          	
                for pt in zip(*self.loc[::-1]):
                   cv2.rectangle(self.imgRGB, pt, (pt[0] + self.w, pt[1] + self.h), (0,0,255), 2)
                # Write a result and showing out.
                cv2.imwrite(self.picRst, self.imgRGB)
                plt.subplot(121),plt.imshow(self.res,cmap = 'gray')
                plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
                plt.subplot(122),plt.imshow(self.imgRGB,cmap = 'gray')
                plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                plt.show()
 
def main(argv):
	inputfile = ''
	templatefile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:t:o:",["ifile=","tfile","ofile="])
	except getopt.GetoptError:
		print 'test.py -i <inputfile> -t <templatefile> -o <outputfile>'
	   	sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
	   		print 'test.py -i <inputfile> -t <templatefile> -o <outputfile>'
	   		sys.exit()
	   	elif opt in ("-i", "--ifile"):
	   		inputfile = arg
	   	elif opt in ("-t", "--tfile"):
	   		templatefile = arg
	   	elif opt in ("-o", "--ofile"):
	   		outputfile = arg
	print 'Input file is "', inputfile
	print 'Template file is "', inputfile
	print 'Output file is "', outputfile
	fox = compareImage(inputfile, templatefile, outputfile)
	fox.compare()
	fox.display()
 
if __name__ == '__main__':
	main(sys.argv[1:])
