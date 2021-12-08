import ChatClient4eval
import argparse
import time
import select
import sys
import os
import json
import getpass
import hashlib

def start_chat(name):
    client = ChatClient4eval.ChatClient(name)
    start_time = time.time()
    client.check_catalog()
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
	args = parser.parse_args()
	start_chat(args.Name)

