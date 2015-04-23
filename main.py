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
	
	argument_parser.add_argument("depth", help="", type=int)

	args = argument_parser.parse_args()

	githubu = args.github

	twiteru = args.twiter

	max_depth = args.depth

	print "crawl the github social graph of %s" % githubu

	matrix_g, nodes_g = github.start(githubu, max_depth)

	print "crawl the twiter social graph of %s" % twiteru

	matrix_t, nodes_t = twiter.start(twiteru, max_depth)

	print "calculate the similarity matrix between github social graph and twiter social graph"

	similarity_matrix = cal_matrix.cal_similarity_matrix(matrix_g, matrix_t)

	print "make decision"

	filters.start(similarity_matrix, nodes_g, nodes_t)




	
