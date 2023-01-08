import threading
import socket
import rsa_module
import rsa

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5678))
server.listen()
clients = []
aliases = []
clients_public_keys = []
leaving = []
server_private_key = rsa_module.read_server_private_key()


# Functions to handle the clients connection
def broadcast(message):
    for client in clients:
        index = clients.index(client)
        clients_public_key = clients_public_keys[index]
        encrypted_message = rsa.encrypt(message.encode(), clients_public_key)
        client.send(encrypted_message)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            decrypted_message = rsa.decrypt(message, server_private_key).decode()
            print(decrypted_message)
            broadcast(decrypted_message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!')
            aliases.remove(alias)
            clients_public_key = clients_public_keys[index]
            clients_public_keys.remove(clients_public_key)
            break


# Main function to receive the clients connection

def receive():
    while True:
        print("Server is running and listening ...")
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        ecpk = client.recv(1024)
        dcpk = rsa.decrypt(ecpk, server_private_key).decode()
        cpk = rsa.PublicKey.load_pkcs1(dcpk)
        aliases.append(alias)
        clients.append(client)
        clients_public_keys.append(cpk)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room')
        client.send('You are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


def send():
    msg = input("Message: ")
    message = f'Server: {msg}'
    broadcast(message)


def list_clients():
    for alias in aliases:
        print(alias)


def choices():
    while True:
        c = input("1- message\n2-list_clients\n3-stop_server")
        if c == "1":
            send()
        elif c == "2":
            list_clients()
        elif c == "3":
            broadcast("Stoping")
            raise Exception("Server closed!")
        else:
            print("Choice must be a number between 1-3")


if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    choices_thread = threading.Thread(target=choices)
    choices_thread.start()
