# -*- coding: utf-8 -*-

import numpy
import random
import argparse

if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(description='')

    argument_parser.add_argument('-p2g', '--path2adjmatg', help='')
    argument_parser.add_argument('-p2t', '--path2adjmatt', help='')

    args = argument_parser.parse_args()

    #读入两个方阵

    if args.path2adjmatg and args.path2adjmatt:

        path2adjmatg = args.path2adjmatg
        path2adjmatt = args.path2adjmatt

    #随机生成两个方阵

    else:

        nodes4g = random.randint(1, 10)

        nodes4t = random.randint(1, 10)

        g = numpy.reshape(numpy.random.random_integers(0, 1, size=nodes4g*nodes4g), (nodes4g, nodes4g))

        t = numpy.reshape(numpy.random.random_integers(0, 1, size=nodes4t*nodes4t), (nodes4t, nodes4t))

        s = numpy.ones((nodes4t, nodes4g), dtype=numpy.int64)

        print g
        print t
        print s

        tmp = numpy.dot(numpy.dot(t, s), g.transpose()) + numpy.dot(numpy.dot(t.transpose(), s), g)

        tmp = tmp / numpy.linalg.norm(tmp)

        print tmp
