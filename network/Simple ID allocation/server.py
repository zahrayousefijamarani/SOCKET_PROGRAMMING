import socket
import threading

numbers = []
clients = []


def handle(client, c_number):
    while True:
        try:
            number = eval(client.recv(1024).decode("ascii"))
            numbers.append(number)  # (client_number , value)
            while len(numbers) % 2 != 0:  # first client is waiting for second
                continue
            s = numbers[0][1] + numbers[1][1]
            client.send(str(s).encode("ascii"))
            numbers.clear()
        except:
            print(f"client {c_number} disconnected")
            client.close()
            break


host = '127.0.0.1'
port = 23005
client_number = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()
print("Listening...")

while True:
    client_socket, address = server.accept()
    print(f"Client {client_number} connected")

    m = ("client_number", client_number)
    client_socket.send(str(m).encode("ascii"))

    clients.append((client_number, client_socket))

    client_number += 1

    thread = threading.Thread(target=handle, args=(client_socket, client_number,))
    thread.start()
