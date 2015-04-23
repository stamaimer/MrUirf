# -*- coding: utf-8 -*-

import twitter.gen_friendship as twiter
import github.gen_friendship as github
import cal_matrix
import filters

import argparse

if __name__ == "__main__":

	argument_parser = argparse.ArgumentParser(description="")
	
	argument_parser.add_argument("github", help="")

	argument_parser.add_argument("twiter", help="")
	
	argument_parser.add_argument("-d", "--depth", help="", type=int)

	argument_parser.add_argument("-i", "--iterations", type=int, help="")

	args = argument_parser.parse_args()

	githubu = args.github

	twiteru = args.twiter

	print "crawl the github social graph of %s" % githubu

	matrix_g, nodes_g = github.start(githubu, args.depth)

	print "crawl the twiter social graph of %s" % twiteru

	matrix_t, nodes_t = twiter.start(twiteru, args.depth)

	print "calculate the similarity matrix between github social graph and twiter social graph"

	if args.iterations:

		similarity_matrix = cal_matrix.cal_similarity_matrix(matrix_g, matrix_t, args.iterations)

	else:

		similarity_matrix = cal_matrix.cal_similarity_matrix(matrix_g, matrix_t)

	print "make decision"

	filters.start(similarity_matrix, nodes_g, nodes_t)




	
