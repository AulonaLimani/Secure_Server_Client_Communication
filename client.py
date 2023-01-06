import Info
import threading
import socket

alias = input("Choose an alias >>> ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((Info.host, Info.port))


def client_recieve():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            elif message == "Stoping":
                print("Server closed!")
                client.close()
            else:
                print(message)
        except:
            client.close()
            break


def client_send():
    while True:
        msg = input("")
        message = f'{alias}: {msg}'
        if msg != "leave":
            client.send(message.encode('utf-8'))
        else:
            client.send(message.encode('utf-8'))
            client.close()
            break


receive_thread = threading.Thread(target=client_recieve)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
