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
	greetings = str(f'| Logged in as: {username} |')
	print("-"*len(greetings))
	print(greetings)
	print("-"*110)
	print("Menu | 1: Show Users | 2: Show Groups | 3: Show Connections | 4: Connect to User | 5: Send Message to User |")
	print("     | 6: Connect to Group | 7: Send Message to Group | 8: Create Group | 9: History | 0: Exit")
	print("-"*110)

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
			print(crypt.crypt(pw))
			print(credentials[username])
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
				print("Current Users")
				client.show_current_users()
			elif choice == '2':
				os.system('clear')
				screenMenu(name)
				print("Current Groups: ")
				client.show_current_groups()
			elif choice == '3':
				os.system('clear')
				screenMenu(name)
				print("Current Connections: ")
				client.show_current_connections()
				client.show_current_group_connections()
			elif choice == '4':
				os.system('clear')
				screenMenu(name)
				print("Avilable Users:")
				client.show_current_users()
				print('Enter the user you would like to connect to:')
				user = input()
				client.request_DM(user)
			elif choice == '5':	
				os.system('clear')
				screenMenu(name)
				print("Avilable Connections:")
				client.show_current_connections()
				print('Enter the user you would like to message:')
				user = input()	
				print('Enter your message to {}:'.format(user))
				message = input()
				client.send_DM(user, message)
			elif choice == '6':
				os.system('clear')
				screenMenu(name)
				print("Avilable Groups:")
				client.show_current_groups()
				print('Enter the group you would like to connect to:')
				user = input()
				client.request_Group(user)
			elif choice == '7':	
				os.system('clear')
				screenMenu(name)
				print("Avilable Connections:")
				client.show_current_group_connections()
				print('Enter the group you would like to message:')
				user = input()	
				print('Enter your message to {}:'.format(user))
				message = input()
				client.send_Group_DM(user, message)
			elif choice == '8':
				os.system('clear')
				screenMenu(name)
				print('Enter the name of the group you want to create:')
				user = input()
				client.create_group(user)
			elif choice == '9':	
				os.system('clear')
				screenMenu(name)
				print("Inbox: \n")
				client.show_chatHistory(name)
			elif choice == '0':	
				quit()

			else:
				os.system('clear')
				print("Invalid Option \n")
				screenMenu(name)
	

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
