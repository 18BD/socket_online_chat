import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

users = []
nicknames = []

def live(message):
	for user in users:
		user.send(message)

def messages(user):
	while True:
		try:
			message = user.recv(1024)
			if '/private' in str(message):
				send_private_msg(message)
			else:
				with open('messages.txt','a') as file:
					file.write(str(message)[2:].replace("'","")+'\n')
				live(message)
		except:
			index = users.index(user)
			users.remove(user)
			user.close()
			nickname = nicknames[index]
			print(f'{nickname} logged out.')
			live(f'{nickname} logged out!'.encode('ascii'))
			nicknames.remove(nickname)
			break

def send_private_msg(message):
	if str(message).split()[2] in nicknames:
		user1 = nicknames.index(str(message).split()[2])
		user2 = nicknames.index(str(message).split()[0][2:].replace(':',''))
		private = [users[user1],users[user2]]
		for user in private:
			user.send(bytes(str(message).split()[0][2:]+' '+str(message)[str(message).index(str(message).split()[2][len(str(message).split()[2])-1:])+2:].replace("'",""), 'utf-8'))

def main():
	print('Chat is ready!')
	with open('messages.txt','w') as file:
		file.write('')
	while True:
		user, address = server.accept()
		user.send('NICK'.encode('ascii'))
		nickname = user.recv(1024).decode('ascii')
		nicknames.append(nickname)
		users.append(user)

		print(f'{nickname} joined to the chat.')
		live(f'{nickname} joined!'.encode('ascii'))
		user.send('You are connected to chat!'.encode('ascii'))

		thread = threading.Thread(target=messages, args=(user,))
		thread.start()

if __name__ == '__main__':
	main()