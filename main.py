# -*- coding: utf-8 -*-

import facebook.gen_friendship as facebook
import twitter.gen_friendship as twitter
import github.gen_friendship as github
import douban.gen_friendship as douban
#import renren.gen_friendship
#import sweibo.gen_friendship

import argparse

if __name__ == "__main__":

	argument_parser = argparse.ArgumentParser(description="")
	
	argument_parser.add_argument("login", help="")
	
	argument_parser.add_argument("depth", help="")

	args = argument_parser.parse_args()

	sed_login = args.login

	max_depth = args.depth

	twitter.start(sed_login, max_depth)

	github.start(sed_login, max_depth)



	
