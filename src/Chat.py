import ChatClient
import argparse
import time
import select
import sys
import os
import json



def screenMenu():
	print("-"*94)
	print("Menu | 1: Show Users | 2: Show Connections | 3: Connect | 4: Send Message | 5. Chat History")
	print("-"*94)


def start_chat(name):

	client = ChatClient.ChatClient(name)
	start_time = time.time()
	while(True):
		client.check_sockets()
		client.check_catalog()
		current_time = time.time()
		t = current_time - start_time
		if t > 60:
			client.update_catalog()
			start_time = time.time()

		i, o, e = select.select( [sys.stdin], [], [], 5 )
		if i:
			choice = sys.stdin.readline().strip()
			if choice == '1':
				os.system('clear')
				screenMenu()
				print("Current Users")
				client.show_current_users()
			elif choice == '2':
				os.system('clear')
				screenMenu()
				print("Current Connections: ")
				client.show_current_connections()
			elif choice == '3':
				os.system('clear')
				screenMenu()
				print("Avilable Users:")
				client.show_current_users()
				print('Enter the user you would like to connect to:')
				user = input()
				client.request_DM(user)
			elif choice == '4':	
				os.system('clear')
				screenMenu()
				print("Avilable Connections:")
				client.show_current_connections()
				print('Enter the user you would like to message:')
				user = input()	
				print('Enter your message to {}:'.format(user))
				message = input()
				client.send_DM(user, message)

			elif choice == '5':	
				os.system('clear')
				screenMenu()
				print("Chat History: \n")
				client.show_chatHistory(name)
			else:
				os.system('clear')
				print("Invalid Option \n")
				screenMenu()
	

if __name__ == "__main__":

	# display menu
	screenMenu()

	# get arguments from users
	parser = argparse.ArgumentParser()
	parser.add_argument('Name')
	args = parser.parse_args()
	
	start_chat(args.Name)
