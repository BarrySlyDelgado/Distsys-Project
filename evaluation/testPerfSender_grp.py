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
	num_ops = 10
	total_time = 0

	client = ChatClient4eval.ChatClient(name)
	start_time = time.time()
	client.check_catalog()
	client.check_sockets()
	client.request_Group(Group)
    
	for count in range(1,num_ops+1):
		current_time = time.time()
		t = current_time - start_time
		if t > 60:
			client.update_catalog()
			start_time = time.time()
		message = f'Sample message {count+1}'
		sent_time = time.time()
		client.check_sockets()
		client.send_Group_DM(Group, message)
		end_time = time.time()


		t = end_time - sent_time
		total_time += t
	print(f'\n For {name} -->>>  throughput = {num_ops/total_time} || latency = {total_time/num_ops}')



		
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('Name')
	parser.add_argument('Group')
	args = parser.parse_args()
	start_chat(args.Name, args.Group)


