import socket
import threading

host = '127.0.0.1'
port = 23005

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.setblocking(True)

client_number = -1


def receive():
    global client_number
    while True:
        try:
            answer = client.recv(1024).decode("ascii")
            if answer.__contains__("client_number"):
                m = eval(answer)
                client_number = m[1]
            else:
                print(answer)
        except:
            client.close()
            break


def write():
    while True:
        try:
            first = float(input("enter your number\n"))
            message = (client_number, first)
            client.send(str(message).encode("ascii"))
        except:
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
