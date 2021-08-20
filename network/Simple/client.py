import socket
import threading

host = '127.0.0.1'
port = 23005

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.setblocking(True)


def receive():
    while True:
        try:
            answer = client.recv(1024).decode("ascii")
            print(answer)
        except:
            client.close()
            break


def write():
    while True:
        try:
            first = float(input("enter first number\n"))
            second = float(input("enter second number\n"))
            message = str((first, second)).encode("ascii")
            client.send(message)
        except:
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
