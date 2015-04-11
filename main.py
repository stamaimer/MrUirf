# -*- coding: utf-8 -*-

import twiter.gen_friendship as twitte
import github.gen_friendship as github
import gen_matpic
import cal_matrix
import leven

import argparse

if __name__ == "__main__":

	argument_parser = argparse.ArgumentParser(description="")
	
	argument_parser.add_argument("login", help="")
	
	argument_parser.add_argument("depth", help="", type=int)

	args = argument_parser.parse_args()

	sed_login = args.login

	max_depth = args.depth

	path2json_graph_g = github.start(sed_login, max_depth)

	path2json_graph_t = twiter.start(sed_login, max_depth)

	matrix_g, nodes_g = gen_matpic.foo(path2json_graph_g, "github")

	matrix_t, nodes_t = gen_matpic.foo(path2json_graph_t, "twiter")

	similarity_matrix = cal_matrix.cal_similarity_matrix(matrix_g, matrix_t)


	
