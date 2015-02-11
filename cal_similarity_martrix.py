import numpy
import argparse

if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(description='')

    argument_parser.add_argument('-p2g', '--path2adjmatg', help='')
    argument_parser.add_argument('-p2t', '--path2adjmatt', help='')

    args = argument_parser.parse_args()

    #读入两个方阵

    if path2adjmatg and path2adjmatt:

        path2adjmatg = args.path2adjmatg
        path2adjmatt = args.path2adjmatt

    #随机生成两个方阵

    else:

        g = numpy.reshape(numpy.random.random_integers(0, 1, size=100), (10, 10))

        t = numpy.reshape(numpy.random.random_integers(0, 1, size=100), (10, 10))
