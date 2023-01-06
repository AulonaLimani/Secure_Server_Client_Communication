import Info
import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((Info.host, Info.port))
server.listen()
clients = []
aliases = []
leaving = []


# Functions to handle the clients connection
def broadcast(message):
    for client in clients:
        client.send(message)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            msg = message.decode('utf-8')
            print(msg)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break


# Main function to receive the clients connection

def receive():
    while True:
        print("Server is running and listening ...")
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('You are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


def send():
    msg = input("Message: ")
    message = f'Server: {msg}'
    broadcast(message.encode('utf-8'))


def list_clients():
    for alias in aliases:
        print(alias)


def close_server():
    broadcast("Stoping".encode('utf-8'))
    raise Exception("Server closed!")


def choices():
    while True:
        c = input("1- message\n2-list_clients\n3-stop_server")
        if c == "1":
            send()
        elif c == "2":
            list_clients()
        else:
            close_server()
            break


if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    choices_thread = threading.Thread(target=choices)
    choices_thread.start()
