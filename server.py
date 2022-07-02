import threading
import socket


HOST = socket.gethostbyname(socket.gethostname())
PORT = 50505

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
print(f'<<SERVER LISTENING ON {HOST}:{PORT}>>')
server.listen(10)

clients = []


class Client:
    def __init__(self, client, address):
        self.client = client
        self.address = address
        self.nick = 'anonymous'


def broadcast(message):
    for client in clients:
        client.client.send(message)


def handle(client):
    while True:
        try:
            message = client.client.recv(1024)
            if message.decode('utf-8') == '/quit':
                client.client.send('/quit'.encode('utf-8'))
                clients.remove(client)
                broadcast(f'<<{client.nick}@{client.address[0]} has quit>>'.encode('utf-8'))
                print(f'{client.address} {client.nick} has quit')
                client.client.close()
                break
            if '/nick' in message.decode('utf-8'):
                new_nick = message.decode('utf-8').split(' ')[1]
                broadcast(f'<<{client.nick}@{client.address[0]} is now known as {new_nick}>>'.encode('utf-8'))
                client.nick = new_nick
            else:
                broadcast(f'{client.nick}@{client.address[0]}: {message.decode("utf-8")}'.encode('utf-8'))
        except:
            clients.remove(client)
            print(f'{client.address} disconnected')
            client.client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        c = Client(client, address)
        clients.append(c)
        print(f'{address} has connected')
        c.client.send('<<you are connected, set nick with "/nick" and "/quit" to leave>>\n'.encode('utf-8'))
        broadcast(f'<<{c.nick}@{c.address[0]} has joined>>'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(c,))
        thread.start()


receive()
