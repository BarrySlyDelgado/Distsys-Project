import ChatClient4eval
import argparse
import time
import select
import sys
import os
import json
import getpass
import hashlib

def start_chat(name, receiver):
	num_ops = 10

	client = ChatClient4eval.ChatClient(name)
	start_time = time.time()
	total_time = 0

	client.check_catalog()
	for count in range(1,num_ops+1):
		current_time = time.time()
		t = current_time - start_time
		if t > 60:
			client.update_catalog()
			start_time = time.time()
		message = f'Sample message {count}'
		
		client.check_sockets()
		client.request_DM(receiver)
		
		sent_time = time.time()
		client.check_sockets()
		client.send_DM(receiver, message)
		end_time = time.time()


		t = end_time - sent_time
		total_time += t
	print(f'\n For {name} -->>>  time = {total_time} throughput = {num_ops/total_time} || latency = {total_time/num_ops}')


if __name__ == "__main__":
	# get arguments from users
	parser = argparse.ArgumentParser()
	parser.add_argument('Name')
	parser.add_argument('Receiver')
	args = parser.parse_args()
	start_chat(args.Name, args.Receiver)

