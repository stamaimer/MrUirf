# -*- coding: utf-8 -*-

import numpy

def topns(matrix, n):

	matrix = numpy.array(matrix)

	flatted = matrix.flatten()

	idx_1d = numpy.argpartition(flatted, -n)[-n:]

	idx_2d = numpy.vstack(numpy.unravel_index(idx_1d, matrix.shape)).transpose()

	idx_2d = reversed(idx_2d)

	# print idx_2d

	# for index in idx_2d:

	# 	print matrix[index[0]][index[1]]

	return idx_2d

def leven(gnodes, tnodes, pairs):

	pass

def start(matrix, gnodes, tnodes):

	# numpy.set_printoptions(threshold="nan")

	# print matrix

	# for node in gnodes:
	
	# 	print node

	# for node in tnodes:
	
	# 	print node

	# print "============================" 

	pairs = topns(matrix, matrix.shape[0] if matrix.shape[0] <= matrix.shape[1] else matrix.shape[1])

	suspect = leven(gnodes, tnodes, pairs)

