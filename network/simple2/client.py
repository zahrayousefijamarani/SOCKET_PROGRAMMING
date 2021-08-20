import socket
import threading

# host = '188.209.77.41'
host = '2.177.67.132'
port = 23005

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.setblocking(True)

user_id = ""

accepted = False


def receive():
    global user_id, accepted
    while True:
        try:
            answer = client.recv(1024).decode("ascii")
            if answer.__contains__("send your user-id"):
                user_id = input("please enter an user-id\n")
                client.send(user_id.encode("ascii"))
            elif answer.__contains__("accepted"):
                accepted = True
            else:
                print(answer)
        except:
            client.close()
            break


def write():
    while True:
        try:
            if accepted:
                command = input("Please enter your command\n")
                client.send(command.encode("ascii"))
        except:
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
