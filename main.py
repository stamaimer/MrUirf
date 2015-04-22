# -*- coding: utf-8 -*-

import twitter.gen_friendship as twiter
import github.gen_friendship as github
import gen_matpic
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

	path2json_graph_g = github.start(githubu, max_depth)

	if path2json_graph_g == None:

		print "%s isn't found!" % githubu

		return

	path2json_graph_t = twiter.start(twiteru, max_depth)

	if path2json_graph_g == None:

		print "%s isn't found!" % twiteru

		return

	matrix_g, nodes_g = gen_matpic.foo(path2json_graph_g, "github")#

	matrix_t, nodes_t = gen_matpic.foo(path2json_graph_t, "twitter")#

	similarity_matrix = cal_matrix.cal_similarity_matrix(matrix_g, matrix_t)

	filters.start(similarity_matrix, gnodes, tnodes)




	
