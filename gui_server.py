import socket
import threading

host = '127.0.0.1'
port = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while True:
		try:
			message = client.recv(1024)
			broadcast(message)
		except:
			index = client.index(client)
			clients.remove(client)
			client.close()
			nickname = nicknames[index]
			nicknames.remove(nickname)
			break

def receive():
	while True:
		client, address = server.accept()
		print(f'Connected with {str(address)}')

		client.send('NICK'.encode('utf-8'))

		nickname = client.recv(1024)

		nicknames.append(nickname)

		clients.append(client)

		broadcast(f'{str(nickname)[2:len(str(nickname))-1]} connected to the server\n'.encode('utf-8'))

		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

print('Server is running...')
receive()