import cv2 

TAG_FLOAT = 202021.25 # check for this when READING a flo file

def readFlo(path): 
	from ctypes import sizeof, c_int, c_float, c_double
	import numpy as np 
	sz_int = sizeof(c_int)
	sz_float = sizeof(c_float)
	sz_double = sizeof(c_double)

	import struct 
	#Read binary .flo file, saved using flowIO::WriteFlowFile()
	fo = open(path, 'rw+')
	tag = struct.unpack('f', fo.read(sz_float))[0]
	matWidth = struct.unpack('i', fo.read(sz_int))[0]
	matHeight = struct.unpack('i', fo.read(sz_int))[0]
			
	nbands = 2
	flo = np.zeros((matWidth, matHeight, 2), dtype = np.float32)
	print "Reading flo image"
	n = nbands*matWidth
	for i in range(matHeight):
		val = np.array(struct.unpack('f'*n, fo.read(sz_float*n)))
		flo[:,i,:] = val.reshape((matWidth, 2))

	fo.close()
	return flo

def readFileToMat(path): 
	from ctypes import sizeof, c_int, c_float, c_double
	import numpy as np 
	sz_int = sizeof(c_int)
	sz_float = sizeof(c_float)
	sz_double = sizeof(c_double)

	import struct 
	#Read binary .mat file, saved using optical_flow_ext.cpp:writeMatToFile()
	fo = open(path, 'rw+')
	arrayType = struct.unpack('i', fo.read(sz_int))[0]
	matWidth = struct.unpack('i', fo.read(sz_int))[0]
	matHeight = struct.unpack('i', fo.read(sz_int))[0]
			
	#FLOAT ONE CHANNEL
	if arrayType == cv2.CV_32F:
		mat = np.zeros((matHeight, matWidth), dtype = np.float32)
		print "Reading CV_32F image"
		for i in range(matHeight):
			for j in range(matWidth):
				val = struct.unpack('f', fo.read(sz_int))[0]
				#if val > 0:
				#	print val 
				mat[i,j] = val
	#DOUBLE ONE CHANNEL
	elif arrayType == cv2.CV_64F:
		mat = np.zeros((matHeight, matWidth), dtype = np.float64)
		print "Reading CV_64F image"
		for i in range(matHeight):
			for j in range(matWidth):
				val = struct.unpack('d', fo.read(sz_double))[0]
				mat[i,j] = val
	#FLOAT THREE CHANNELS
	elif arrayType == cv2.CV_32FC3:
		mat = np.zeros((matHeight, matWidth), dtype = np.float32);
		print "Reading CV_32FC3 image"
		for i in range(matHeight):
			for j in range(matWidth):
				val = struct.unpack('f', fo.read(sz_float))[0]
				mat[i,j] = val
	#DOUBLE THREE CHANNELS
	elif arrayType == cv2.CV_64FC3:
		mat = np.zeros((matHeight, matWidth), dtype = np.float64)
		print "Reading CV_64FC3 image"
		for i in range(matHeight):
			for j in range(matWidth):
				val = struct.unpack('d', fo.read(sz_double))[0]
				mat[i,j] = val
	else:
		print "Error: wrong Mat type: must be CV_32F, CV_64F, CV_32FC3 or CV_64FC3"

	fo.close()
	return mat

def type2str(type):
	#depth = chr(type & CV_MAT_DEPTH_MASK)
	#chans = chr(1 + (type >> CV_CN_SHIFT))
	depth = (type & CV_MAT_DEPTH_MASK)
	chans = (1 + (type >> CV_CN_SHIFT))
	if depth == cv2.CV_8U:
		r = "8U"
	elif depth == cv2.CV_8S:
		r = "8S"
	elif depth == cv2.CV_16U:
		r = "16U"
	elif depth == cv2.CV_16S:
		r = "16S"
	elif depth == cv2.CV_32S:
		r = "32S"
	elif depth == cv2.CV_32F:
		r = "32F"
	elif depth == cv2.CV_64F:
		r = "64F"
	else:
		r = "User"
	r += "C"
	r += (str(chans)+'0')
	return r

###From http://www.pyimagesearch.com/2015/08/10/checking-your-opencv-version-using-python/
def is_cv2():
    # if we are using OpenCV 2, then our cv2.__version__ will start
    # with '2.'
    return check_opencv_version("2.")
 
def is_cv3():
    # if we are using OpenCV 3.X, then our cv2.__version__ will start
    # with '3.'
    return check_opencv_version("3.")
 
def check_opencv_version(major, lib=None):
    # if the supplied library is None, import OpenCV
    if lib is None:
        import cv2 as lib
        
    # return whether or not the current OpenCV version matches the
    # major version number
    return lib.__version__.startswith(major)