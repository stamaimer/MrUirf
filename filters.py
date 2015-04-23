# -*- coding: utf-8 -*-

import numpy

def topns(matrix, n):

	numpy.set_printoptions(threshold="nan")

	print matrix

	flatted = matrix.flatten()

	idx_1d = numpy.argpartition(flatted, -n)[-n:]

	x_idx, y_idx = numpy.unravel_index(idx_1d, matrix.shape)

	for x, y in zip(x_idx, y_idx):

		print matrix[x][y]

def leven(gnodes, tnodes):

	pass

def start(matrix, gnodes, tnodes):

	topns(matrix, 3)