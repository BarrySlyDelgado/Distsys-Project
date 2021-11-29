import ChatClient
import argparse
import time
import select
import sys
import os
import json



def screenMenu():
	print("-"*94)
	print("Menu | 1: Show Users | 2: Show Groups | 3: Show Connections | 4: Connect to User | 5: Send Message to User | 6: Connect to Group | 7: Send Message to Group | 8: Create Group | 9: Chat History")
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
				print("Current Groups: ")
				client.show_current_groups()
			elif choice == '3':
				os.system('clear')
				screenMenu()
				print("Current Connections: ")
				client.show_current_connections()
				client.show_current_group_connections()
			elif choice == '4':
				os.system('clear')
				screenMenu()
				print("Avilable Users:")
				client.show_current_users()
				print('Enter the user you would like to connect to:')
				user = input()
				client.request_DM(user)
			elif choice == '5':	
				os.system('clear')
				screenMenu()
				print("Avilable Connections:")
				client.show_current_connections()
				print('Enter the user you would like to message:')
				user = input()	
				print('Enter your message to {}:'.format(user))
				message = input()
				client.send_DM(user, message)
			elif choice == '6':
				os.system('clear')
				screenMenu()
				print("Avilable Users:")
				client.show_current_groups()
				print('Enter the group you would like to connect to:')
				user = input()
				client.request_Group(user)
			elif choice == '7':	
				os.system('clear')
				screenMenu()
				print("Avilable Connections:")
				client.show_current_group_connections()
				print('Enter the group you would like to message:')
				user = input()	
				print('Enter your message to {}:'.format(user))
				message = input()
				client.send_Group_DM(user, message)
			elif choice == '8':
				os.system('clear')
				screenMenu()
				print('Enter the name of the group you want to create:')
				user = input()
				client.create_group(user)
			elif choice == '9':	
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
