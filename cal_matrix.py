# -*- coding: utf-8 -*-

import numpy
import random
import argparse

def cal_similarity_matrix(g, t, iterations=100):

    s = numpy.ones((t.shape[0], g.shape[0]), dtype=numpy.int64)

    for i in range(iterations):

        tmp = numpy.dot(numpy.dot(t, s), g.transpose()) + numpy.dot(numpy.dot(t.transpose(), s), g)

        tmp = tmp / numpy.linalg.norm(tmp)

        s = tmp

    return tmp

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("-p2g", "--path2adjmatg", help="")
    argument_parser.add_argument("-p2t", "--path2adjmatt", help="")
    argument_parser.add_argument("-i", "--iterations", type=int, help="")

    args = argument_parser.parse_args()

    #读入两个方阵

    if args.path2adjmatg and args.path2adjmatt:

        path2adjmatg = args.path2adjmatg
        path2adjmatt = args.path2adjmatt

        g = numpy.loadtxt(path2adjmatg, dtype=numpy.int64, delimiter=',')
        t = numpy.loadtxt(path2adjmatt, dtype=numpy.int64, delimiter=',')

    #随机生成两个方阵

    else:

        nodes4g = random.randint(1, 10)
        nodes4t = random.randint(1, 10)

        g = numpy.reshape(numpy.random.random_integers(0, 1, size=nodes4g*nodes4g), (nodes4g, nodes4g))
        t = numpy.reshape(numpy.random.random_integers(0, 1, size=nodes4t*nodes4t), (nodes4t, nodes4t))

    if args.iterations:

        cal_similarity_matrix(g, t, args.iterations)

    else:

        cal_similarity_matrix(g, t)
