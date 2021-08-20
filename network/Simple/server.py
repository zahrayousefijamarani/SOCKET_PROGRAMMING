import socket
import threading


def handle(client):
    while True:
        try:
            numbers = eval(client.recv(1024).decode("ascii"))
            s = numbers[0] + numbers[1]
            client.send(str(s).encode("ascii"))
        except:
            print("client disconnected")
            client.close()
            break


host = '127.0.0.1'
port = 23005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()
print("Listening...")

while True:
    client_socket, address = server.accept()
    print("Client connected")
    thread = threading.Thread(target=handle, args=(client_socket,))
    thread.start()
