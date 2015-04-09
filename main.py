# -*- coding: utf-8 -*-

import twiter.gen_friendship as twiter
import github.gen_friendship as github
import gen_matpic
import cal_matrix

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

	path2matrix_g, path2image_g, path2nodes_g = gen_matpic.foo(path2json_graph_g, "github")

	path2matrix_t, path2image_t, path2nodes_t = gen_matpic.foo(path2json_graph_t, "twiter")

	cal_matrix.cal_similarity_matrix(path2matrix_g, path2matrix_t)


	
