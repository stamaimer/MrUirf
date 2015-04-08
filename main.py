# -*- coding: utf-8 -*-

import twitter.gen_friendship as twitter
import github.gen_friendship as github
import gen_matpic
import cal_matrix

import argparse

if __name__ == "__main__":

	argument_parser = argparse.ArgumentParser(description="")
	
	argument_parser.add_argument("login", help="")
	
	argument_parser.add_argument("depth", help="")

	args = argument_parser.parse_args()

	sed_login = args.login

	max_depth = args.depth

	tjpath = twitter.start(sed_login, max_depth)

	gjpath = github.start(sed_login, max_depth)

	tmpath = gen_matpic.foo(tjpath, "twitter")

	gmpath = gen_matpic.foo(gjpath, "github")

	cal_matrix(tmpath, gmpath)

	
