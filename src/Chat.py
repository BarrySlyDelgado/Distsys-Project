import ChatClient
import argparse
import time
import select
import sys
import os
import json
import getpass
import hashlib


def screenMenu(username):
	greetings = str(f'|Logged in as: {username}|')
	print("-"*len(greetings))
	print(greetings)
	print("-"*91)
	print("Menu | 1: Online Users/Groups | 2: My Connections      | 3: Create Group     |")
	print("     | 4: Connect to User     | 5: Connect to Group    | 6: Message User     | 0: Sign Out")
	print("     | 7: Message Group       | 8: Show Personal Chats | 9: Show Group Chats |")
	print("-"*91)

def login_auth(username):
	account_list = []
	credentials = {}
	
	if os.path.exists("users.txt") == True:
		f = open("users.txt",'r')
		filedata = f.read()
		f.close()
		credentials = json.loads(filedata)
		account_list = list(credentials.keys())
	if username in account_list:
		pw = getpass.getpass('Password :: ')
		if 	hashlib.sha224(bytes(pw,'utf-8')).hexdigest() == credentials[username]:
			return "sucess"
		else:
			print("Incorrect Password !! login failed !!")
			return "failed"
	
	else:
		print("New User, type in the desired pw for your account: ")
		pw2 = ''
		pw = '1'
		while(pw != pw2):
			pw = getpass.getpass('Password :: ')
			print("Confirm password: ")
			pw2 = getpass.getpass('Password :: ')
			if pw != pw2:
				print("Entered passwords do not match, try again !!")
		credentials[username] = hashlib.sha224(bytes(pw,'utf-8')).hexdigest()
		f = open("users.temp",'w')
		f.write(json.dumps(credentials))
		f.close
		os.rename("users.temp","users.txt")
		print(f'New user account created with username: {username}')
		return "sucess"

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
				screenMenu(name)
				print("Current Users:")
				print("----------------------------------")
				client.show_current_users()
				print("\nCurrent Groups: ")
				print("----------------------------------")
				client.show_current_groups()

			elif choice == '2':
				os.system('clear')
				screenMenu(name)
				print("Connected Users:")
				print("----------------------------------")
				client.show_current_connections()
				print("\nConnected Groups: ")
				print("----------------------------------")
				client.show_current_group_connections()
			
			elif choice == '3':
				os.system('clear')
				screenMenu(name)
				print('Enter the name of the group you want to create:')
				user = input()
				client.create_group(user)

			elif choice == '4':
				os.system('clear')
				screenMenu(name)
				print("Avilable Users:")
				print("----------------------------------")
				client.show_current_users()
				print('\nEnter the user you would like to connect to:')
				user = input()
				if user not in client.user_list:
					print("\nInvalid Selection, press 4 to try again, or choose from menu.")
				else:
					client.request_DM(user)

			elif choice == '5':
				os.system('clear')
				screenMenu(name)
				print("Avilable Groups:")
				print("----------------------------------")
				client.show_current_groups()
				print('\nEnter the group you would like to connect to:')
				user = input()
				if user not in client.group_list:
					print("\nInvalid Selection, press 5 to try again, or choose from menu.")
				else:
					client.request_Group(user)

			elif choice == '6':	
				os.system('clear')
				screenMenu(name)
				print("Connected Users:")
				print("----------------------------------")
				client.show_current_connections()
				if len(list(client.accepted_connections.keys())) == 0:
					print("No conneted users to send message !!")
				else:
					print('\nEnter the user you would like to message:')
					user = input()	
					if user not in client.accepted_connections:
						print("\nInvalid Selection, press 6 to try again, or choose from menu.")
					else:
						print('\nEnter your message to {}:'.format(user))
						message = input()
						client.send_DM(user, message)

				
			elif choice == '7':	
				os.system('clear')
				screenMenu(name)
				print("Connected Group:")
				print("----------------------------------")
				client.show_current_group_connections()
				if len(list(client.accepted_group_connections.keys())) == 0 and len(list(client.group_sockets.keys())) == 0:
					print("No conneted groups to send message !!")
				else:
					print('\nEnter the group you would like to message:')
					user = input()	
					if user not in client.accepted_group_connections and user not in client.group_sockets:
						print("\nInvalid Selection, press 7 to try again, or choose from menu.")
					else:
						print('\nEnter your message to {}:'.format(user))
						message = input()
						client.send_Group_DM(user, message)

			elif choice == '8':	
				os.system('clear')
				screenMenu(name)
				print("Personal Messages: \n")
				client.show_chat_personal(name)

			elif choice == '9':	
				os.system('clear')
				screenMenu(name)
				print("Group Messages: \n")
				client.show_chat_group(name)

			elif choice == '0':	
				client.logout(name)
				print("----------------------------------")
				print("Sucessfully Logged out !!")
				print("----------------------------------")

				quit()

			else:
				os.system('clear')
				screenMenu(name)
				print("Invalid Option")
	

if __name__ == "__main__":
	user_name = input("Enter Username:: ")

	# authenticate login
	login_status = login_auth(user_name)
	if login_status != "sucess":
		quit()

	# display menu
	os.system('clear')
	screenMenu(user_name)

	# start chat
	start_chat(user_name)
