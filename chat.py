import socket
import threading

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def get_message():
	while True:
		try:
			message = client.recv(1024).decode('ascii')
			if message == 'NICK':
				client.send(nickname.encode('ascii'))
			else:
				print(message)
		except:
			print("Error :/")
			client.close()
			break

def send_message():
	while True:
		message = '{}: {}'.format(nickname, input(''))
		client.send(message.encode('ascii'))

get_message_thread = threading.Thread(target=get_message)
get_message_thread.start()

send_message_thread = threading.Thread(target=send_message)
send_message_thread.start()