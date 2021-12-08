import ChatClient4eval
import argparse
import time
import select
import sys
import os
import json
import getpass
import hashlib

def start_chat(name, Group):

	client = ChatClient4eval.ChatClient(name)
	start_time = time.time()
	total_time = 0

	client.check_catalog()
	client.check_sockets()

	# create group
	client.create_group(Group)

	while(True):
		client.check_sockets()
		current_time = time.time()
		t = current_time - start_time
		if t > 60:
			client.update_catalog()
			start_time = time.time()


if __name__ == "__main__":
	# get arguments from users
	parser = argparse.ArgumentParser()
	parser.add_argument('Name')
	parser.add_argument('Group')
	args = parser.parse_args()
	start_chat(args.Name, args.Group)

