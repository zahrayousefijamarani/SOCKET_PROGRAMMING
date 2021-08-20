import socket
import threading
from random import randint
from time import sleep

host = '127.0.0.1'
ports = [23000, 23001, 23002, 23003, 23004]
my_number = int(input("please enter client number\n")) - 1  # 1 or 2 or 3 or 4 or 5
my_id = randint(0, 1000)
print(my_id)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # me
server.bind((host, ports[my_number]))
server.listen()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # for connecting next


last_id = -1
leader_found = False
leader_m = ""


def receive():  # there is just on client, we don't need while
    global last_id, leader_found, leader_m
    last_client, address = server.accept()
    while True:
        try:
            m = last_client.recv(1024).decode("ascii")
            print(m)
            if m.__contains__("client-id") or m.__contains__("leader"):
                leader_found = True
                leader_m = m   # found server .....
            else:
                last_id = int(m)
        except:
            last_client.close()
            break


def write():
    while True:  # try to connect next one
        try:
            client.connect((host, ports[(my_number + 1) % 5]))
        except:
            continue
        break
    print("connected to next client")
    while True:
        try:
            if not leader_found:
                answer = last_id
                if answer < my_id:
                    client.send(str(my_id).encode("ascii"))
                elif answer > my_id:
                    client.send(str(answer).encode("ascii"))
                else:
                    client.send(str(f"client-id {my_id} is leader").encode("ascii"))
            else:
                client.send(leader_m.encode("ascii"))
            sleep(1)
        except:
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
