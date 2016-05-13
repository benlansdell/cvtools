import cv2 

def readFileToMat(path): 
	from ctypes import sizeof, c_int, c_float, c_double
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