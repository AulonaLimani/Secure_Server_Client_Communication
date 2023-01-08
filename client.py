import threading
import socket
import rsa_module
import rsa
import time

alias = input("Choose an alias >>> ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5678))
keys = rsa_module.generate_public_private_rsa_keys()
server_public_key = rsa_module.read_server_public_key()


def client_recieve():
    while True:
        try:
            message = client.recv(1024)

            try:
                decrypted_message = message.decode()
            except Exception:
                decrypted_message = rsa.decrypt(message, keys['private']).decode()

            if decrypted_message == 'alias?':
                client.send(alias.encode('utf-8'))
                espk = rsa.encrypt(keys['public'].save_pkcs1("PEM"), server_public_key)
                client.send(espk)
            elif decrypted_message == "Stoping":
                print("Server closed!")
                client.close()
            else:
                print(decrypted_message)
        except:
            client.close()
            break


def client_send():
    while True:
        time.sleep(0.07)
        msg = input("Mesazhi :> ")
        message = f'{alias}: {msg}'
        encrypted_message = rsa.encrypt(message.encode(), server_public_key)
        if msg != "leave":
            client.send(encrypted_message)
        else:
            client.send(encrypted_message)
            print("Leaving...")
            client.close()
            break


if __name__ == "__main__":

    receive_thread = threading.Thread(target=client_recieve)
    receive_thread.start()

    send_thread = threading.Thread(target=client_send)
    send_thread.start()
