# -*- coding: utf-8 -*-

import numpy

def topns(matrix, N):

	flatted = matrix.flatten()

	idx_1d = flatted.argsort()[-N:]

	x_idx, y_idx = numpy.unravel_index(idx_1d, matrix.shape)

	print x_idx, y_idx

	# for x, y in zip(x_idx, y_idx):

	# 	print x, y, matrix[x][y]

	# 	print "----------------------------"

def leven(gnodes, tnodes):

	pass

def start(matrix, gnodes, tnodes):

	numpy.set_printoptions(threshold="nan")

	print matrix

	# for node in gnodes:
	
	# 	print node

	# for node in tnodes:
	
	# 	print node

	print "============================" 

	topns(matrix, 3)