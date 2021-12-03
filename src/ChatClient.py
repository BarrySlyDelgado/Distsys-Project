import socket
import json
import select
import subprocess
import time
import os
from subprocess import DEVNULL, STDOUT, check_call # nick added
from datetime import datetime

class ChatClient(object):
	
	def __init__(self, name):
		self.name = name
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((socket.gethostname(), 0))
		self.socket.listen(5)
		self.socket_list = {self.socket}
		self.user_list = {}
		self.group_list = {}
		self.group_sockets = {}
		self.accepted_connections = {}
		self.accepted_group_connections = {}
		self.update_catalog()
		
	def show_current_users(self):
		for user in self.user_list:
			print(user)

	def show_current_groups(self):
		for user in self.group_list:
			print(user)

	def show_current_connections(self):
		print('Current Conncted Users:  ')
		for user in self.accepted_connections:
			print(user)

	def show_current_group_connections(self):
		print('Current Connected Groups:  ')	
		for user in self.accepted_group_connections:
			print(user)
		for user in self.group_sockets:
			print(user)

	def update_catalog(self):
		data = {"type" : "nsbs2-user", "owner" : self.name, "port" : self.socket.getsockname()[1], "project":self.name}
		catalog_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		data = json.dumps(data)
		data = data.encode('utf_8')
		catalog_socket.sendto(data, ('catalog.cse.nd.edu', 9097))

		for group in self.group_sockets:
			data = {"type" : "nsbs2-group", "owner" : self.name, "port" : self.group_sockets[group]['socket'].getsockname()[1], "project":group}
			data = json.dumps(data)
			data = data.encode('utf_8')
			catalog_socket.sendto(data, ('catalog.cse.nd.edu', 9097))

	def check_catalog(self):
		#print('Looking for users....') # uncomment this
		subprocess.check_call(['curl', 'http://catalog.cse.nd.edu:9097/query.json', '--output', 'catalog'], stdout=DEVNULL, stderr=DEVNULL)    
		f = open('catalog')                                                                                   
		data = json.load(f)
		users  = [x for x in data if 'type' in x and (x['type'] == 'nsbs2-user')]
		for user in users:
			name = user['owner']
			port = user['port']
			server = user['name']
			node_type = user['type']
			self.user_list[name] = {'server':server, 'port':port, 'type':node_type}         

		groups  = [x for x in data if 'type' in x and (x['type'] == 'nsbs2-group')]
		for group in groups:
				name = group['project']
				port = group['port']
				server = group['name']
				node_type = group['type']
				owner = group['owner']
				self.group_list[name] = {'server':server, 'port':port, 'type':node_type, 'owner':owner}         

	def create_group(self, name):
		
		new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		new_socket.bind((socket.gethostname(), 0))
		new_socket.listen(5)

		self.group_sockets[name] = {"socket":new_socket, 'port': new_socket.getsockname()[1], "users": {}}
		self.socket_list.add(new_socket)

		data = {"type" : "nsbs2-group", "owner" : self.name, "port" : new_socket.getsockname()[1], "project":name}
		catalog_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		data = json.dumps(data)
		data = data.encode('utf_8')
		catalog_socket.sendto(data, ('catalog.cse.nd.edu', 9097))
		print('Created a group named {}'.format(name))	
		
	def send_DM(self, user, message):
		if user in self.accepted_connections:
			msg = {'method':'DM', 'name':self.name, 'message':str(message)}
			msg = json.dumps(msg)
			msg = msg.encode('utf_8')
			header = '{}:'.format(len(msg))
			msg = header.encode('utf_8') + msg
			self.accepted_connections[user].sendall(msg)


			# write to file
			fileName = "history.txt"
			file2w = open(fileName,'a')
			chat_log = {}
			chat_log["date_time"] = datetime.now().strftime("%b-%d-%Y, %H:%M:%S")
			chat_log["sender"] = self.name
			chat_log["receiver"] = user
			chat_log["message"] = message
			json.dump(chat_log,file2w)
			file2w.write('\n')
			file2w.flush()	
			os.fsync(file2w.fileno())
			file2w.close()
		else:
			print('Unable to send message. User {} is either unknown or has not accepted request.'. format(user))

	def send_Group_DM(self, user, message):
		if user in self.accepted_group_connections:
			msg = {'method':'Send_Group_DM', 'name':self.name, 'message':str(message), 'group':user}
			msg = json.dumps(msg)
			msg = msg.encode('utf_8')
			header = '{}:'.format(len(msg))
			msg = header.encode('utf_8') + msg
			self.accepted_group_connections[user].sendall(msg)

			# write to file
			fileName = "history.txt"
			file2w = open(fileName,'a')
			chat_log = {}
			chat_log["date_time"] = datetime.now().strftime("%b-%d-%Y, %H:%M:%S")
			chat_log["sender"] = self.name
			chat_log["receiver"] = user
			chat_log["message"] = message
			json.dump(chat_log,file2w)
			file2w.write('\n')
			file2w.flush()
			os.fsync(file2w.fileno())
			file2w.close()

		elif user in self.group_sockets:
			group = user
			print("\n")
			print("*"*94)
			print(f'Group DM From {self.name} in group {user}: \n \t {message}')
			print("*"*94)
			msg = {'method':'Group_DM', 'name':self.name, 'message':str(message), 'group':user}
			msg = json.dumps(msg)
			msg = msg.encode('utf_8')
			header = '{}:'.format(len(msg))
			msg = header.encode('utf_8') + msg
			for x in self.group_sockets[group]['users']:
				self.group_sockets[group]['users'][x].sendall(msg)

                        # write to file
			fileName = "history.txt"
			file2w = open(fileName,'a')
			chat_log = {}
			chat_log["date_time"] = datetime.now().strftime("%b-%d-%Y, %H:%M:%S")
			chat_log["sender"] = self.name
			chat_log["receiver"] = user
			chat_log["message"] = message
			json.dump(chat_log,file2w)
			file2w.write('\n')
			file2w.flush()
			os.fsync(file2w.fileno())
			file2w.close()

		else:
			print('Unable to send message. User {} is either unknown or has not accepted request.'. format(user))

	def request_DM(self, user):	
		if user in self.user_list:
			msg = {'method':'Request', 'name':self.name}
			msg = json.dumps(msg)
			msg = msg.encode('utf_8')
			header = '{}:'.format(len(msg))
			msg = header.encode('utf_8') + msg
			server = self.user_list[user]['server']
			port = self.user_list[user]['port']
			req_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				print('connecting to {} on server {} on port {}'.format(user, server, port))
				req_socket.connect((server, port))
				req_socket.sendall(msg)
				self.socket_list.add(req_socket)
				print('Sent request to {}'.format(user))
			except socket.error:
				print('Unable to Connect to user {}'.format(user))	
		else:
			print('User {} is unknown.'.format(user))
			
	def request_Group(self, user):	
		if user in self.group_list:
			msg = {'method':'Group_Request', 'name':self.name, 'group':user}
			msg = json.dumps(msg)
			msg = msg.encode('utf_8')
			header = '{}:'.format(len(msg))
			msg = header.encode('utf_8') + msg
			server = self.group_list[user]['server']
			port = self.group_list[user]['port']
			req_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				print('connecting to {} on server {} on port {}'.format(user, server, port))
				req_socket.connect((server, port))
				req_socket.sendall(msg)
				self.socket_list.add(req_socket)
				print('Your request to join group {} has been sent.'.format(user))
			except socket.error:
				print('Unable to Connect to group {}'.format(user))	
		else:
			print('Group {} is unknown.'.format(user))
	
	def handle_msg(self, msg, socket):
		method = msg['method']
		name = msg['name']
		if method == 'Request':
			print('DM Request From {}...'.format(name))
			print('accept DM request from {}? [y/n]...'.format(name))
			choice = input()
			if choice == 'n':
				return_msg = {'method':'Response', 'name':self.name, 'Response':'n'}
				return_msg = json.dumps(return_msg)
				return_msg = return_msg.encode('utf_8')
				header = '{}:'.format(len(return_msg))
				return_msg = header.encode('utf_8') + return_msg
				socket.sendall(return_msg)
				self.socket_list.remove(socket)
			elif choice == 'y':
				self.accepted_connections[name] = socket
				return_msg = {'method':'Response', 'name':self.name, 'Response':'y'}
				return_msg = json.dumps(return_msg)
				return_msg = return_msg.encode('utf_8')
				header = '{}:'.format(len(return_msg))
				return_msg = header.encode('utf_8') + return_msg

				socket.sendall(return_msg)
		elif method == 'Group_Request':
			group = msg['group']
			print('Request to join group {} From {}...'.format(group, name))
			print('Accept request From {} to join group {}? [y/n]...'.format(name, group))
			choice = input()
			if choice == 'n':
				return_msg = {'method':'Response_Group', 'name':group, 'Response':'n'}
				return_msg = json.dumps(return_msg)
				return_msg = return_msg.encode('utf_8')
				header = '{}:'.format(len(return_msg))
				return_msg = header.encode('utf_8') + return_msg
				socket.sendall(return_msg)
				self.socket_list.remove(socket)
			elif choice == 'y':
				self.group_sockets[group]['users'][name] = socket
				return_msg = {'method':'Response_Group', 'name':group, 'Response':'y'}
				return_msg = json.dumps(return_msg)
				return_msg = return_msg.encode('utf_8')
				header = '{}:'.format(len(return_msg))
				return_msg = header.encode('utf_8') + return_msg
				socket.sendall(return_msg)

		elif method == 'Response':
			response = msg['Response']
			if response == 'y':
				print('Messging Request from {} has been ACCEPTED.'.format(name))
				self.accepted_connections[name] = socket
			elif response == 'n':
				print('Messaging Request from {} has been DECLINED.'.format(name))
				self.socket_list.remove(socket)

		elif method == 'Response_Group':
			response = msg['Response']
			if response == 'y':
				print('Your request to join group {} has been ACCEPTED.'.format(name))
				self.accepted_group_connections[name] = socket
			elif response == 'n':
				print('Your request to join group {} has been DECLINED.'.format(name))
				self.socket_list.remove(socket)
 
		elif method == 'DM':
			x = [x for x in self.accepted_connections if self.accepted_connections[x] == socket]
			if not x:
				print('Message from {} has been declined as they have not been accepted'.format(user))

			else:	
				message = msg['message']
				print("\n")
				print("*"*94)
				print(f'DM From {name}: \n \t {message}')
				print("*"*94)

		elif method == 'Group_DM':
			x = [x for x in self.accepted_group_connections if self.accepted_group_connections[x] == socket]
			if not x:
				print('Message from {} has been declined as they have not been accepted'.format(user))

			else:
				group = msg['group']
				message = msg['message']
				print("\n")
				print("*"*94)
				print(f'Group DM From {name} in group {group}: \n \t {message}')
				print("*"*94)

		elif method == 'Send_Group_DM':
			group = msg['group']
			if name not in self.group_sockets[group]['users']:
				print('Message from {} has been declined as they have not been accepted'.format(user))
			else:
				message = msg['message']
				print("\n")
				print("*"*94)
				print(f'Group DM From {name} in group {group}: \n \t {message}')
				print("*"*94)

				msg = {'method':'Group_DM', 'name':name, 'message':str(message), 'group':group}
				msg = json.dumps(msg)
				msg = msg.encode('utf_8')
				header = '{}:'.format(len(msg))
				msg = header.encode('utf_8') + msg
				for user in self.group_sockets[group]['users']:
					self.group_sockets[group]['users'][user].sendall(msg)
							
	def check_sockets(self):
		#print('checking open sockets...') # uncomment this
		readable, writable, exceptional = select.select(list(self.socket_list), [], list(self.socket_list), 2)
		group_sockets = [self.group_sockets[x]['socket'] for x in self.group_sockets]
		for read_socket in readable:                                                                  
			if read_socket == self.socket:
				print('accepting incomming connection...')
				(clientsocket, address) = read_socket.accept()
				self.socket_list.add(clientsocket)
			elif read_socket in group_sockets:
				(clientsocket, address) = read_socket.accept()
				self.socket_list.add(clientsocket)
			else:
				clientsocket = read_socket

				header = b''
				closed = False
				while ':' not in header.decode('utf_8'):
					msg = clientsocket.recv(1)
					if not msg:
						print('A Socket has been closed...')
						self.socket_list.remove(clientsocket)
						closed = True
						break
					header += msg

				if not closed:
					size = int(header.decode('utf_8').split(':')[0])
					msg = ''
					while size > 0:
						rsp = clientsocket.recv(size)
						x = len(rsp)
						size -= x
						msg += rsp.decode('utf_8')
					msg = json.loads(msg)
					self.handle_msg(msg, clientsocket)

	def show_chatHistory(self,name):
		messages = []
		accepted_groups = ["testgroup1"] # edit this to get accepted groups list
		if os.path.exists("history.txt") == True:
			f = open("history.txt",'r')
			fileData = f.readlines()
			for line in fileData:
				messages.append(json.loads(line))
			for msg in messages:
				if msg["sender"]==name and msg["receiver"] in accepted_groups:
					print(f'You sent a group message to {msg["receiver"]} @ {msg["date_time"]} \n \t {msg["message"]} \n')
				elif msg["receiver"] in accepted_groups:
					print(f'{msg["sender"]} sent a group message to {msg["receiver"]} @ {msg["date_time"]} \n \t {msg["message"]} \n')
				elif msg["receiver"]==name:
					print(f'{msg["sender"]} messaged you @ {msg["date_time"]} \n \t {msg["message"]} \n')
				elif msg["sender"]==name:
					print(f'You messaged {msg["receiver"]} @ {msg["date_time"]} \n \t {msg["message"]} \n')
				
			f.close()
			
	
