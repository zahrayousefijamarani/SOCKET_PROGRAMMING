import re
import socket
import threading

clients = []
groups = []
channels = []


class Group:
    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.members = []
        self.add_member(user_id)

    def add_member(self, user_id):
        for c in clients:
            if c[0] == user_id:
                self.members.append(c)
                break


class Channel:
    def __init__(self, channel_id, user_id):
        self.channel_id = channel_id
        self.admin = user_id
        self.members = []
        self.add_member(user_id)

    def add_member(self, user_id):
        for c in clients:
            if c[0] == user_id:
                self.members.append(c)
                break


def handle(client, user_id):
    while True:
        try:
            server_message = "Failed"
            message = client.recv(1024).decode("ascii")
            if re.search("create group .+", str(message)):
                g_id = str(message)[13:]
                unique_g = True
                for g in groups:
                    if g.group_id == g_id:
                        unique_g = False
                        break
                if unique_g:
                    g = Group(g_id, user_id)
                    groups.append(g)
                    server_message = "Group created"
                else:
                    server_message = "Group-id is not unique"
            elif re.search("join group .+", str(message)):
                g_id = str(message)[11:]
                group = None
                for g in groups:
                    if g.group_id == g_id:
                        group = g
                        break
                if group is None:
                    server_message = "There is no group with this group-id"
                else:
                    group.add_member(user_id)
                    server_message = "joined"
            elif re.search("send message to .+ '.+'", str(message)):
                s = str(message)[16:].split(' ', 1)
                id = s[0]
                m = s[1]
                handled = False
                for c in clients:  # ------------------------- user -----------------
                    if c[0] == id:
                        c[1].send(str((f"private message, user-id:{user_id}", m)).encode("ascii"))
                        server_message = "message sent"
                        handled = True
                if not handled:  # ---------------------------- group----------------
                    has_joined = False
                    for g in groups:
                        if g.group_id == id:
                            for c in g.members:
                                if c[0] == user_id:
                                    has_joined = True
                                    break
                            if has_joined:
                                for c in g.members:
                                    c[1].send(str((f"group-id:{id}, user-id : {user_id}"
                                                   , m)).encode("ascii"))  # all users in group can see message
                                server_message = "message sent"
                            else:
                                server_message = "you are not in group"
                            handled = True
                            break
                    if not handled:
                        for ch in channels:  # ----------------- channel----------------
                            if ch.channel_id == id:
                                if ch.admin == user_id:
                                    for c in ch.members:
                                        c[1].send(str((f"channel-id:{id}, user-id : {user_id}"
                                                       , m)).encode("ascii"))  # all users in channel can see message
                                        server_message = "message sent"
                                else:
                                    server_message = "you are not admin"
                                handled = True
                                break
                    if not handled:
                        server_message = "id was wrong"
            elif re.search("create channel .+", str(message)):
                ch_id = str(message)[15:]
                unique_g = True
                for ch in channels:
                    if ch.channel_id == ch_id:
                        unique_g = False
                        break
                if unique_g:
                    ch = Channel(ch_id, user_id)
                    channels.append(ch)
                    server_message = "Channel created"
                else:
                    server_message = "Channel-id is not unique"
            elif re.search("join channel .+", str(message)):
                ch_id = str(message)[13:]
                channel = None
                for ch in channels:
                    if ch.channel_id == ch_id:
                        channel = ch
                        break
                if channel is None:
                    server_message = "There is no channel with this channel-id"
                else:
                    channel.add_member(user_id)
                    server_message = "joined"
            else:
                server_message = "your command was wrong"
            client.send(server_message.encode("ascii"))
        except:
            print(f"client {user_id} disconnected")
            client.close()
            break


host = ''
# host = '127.0.0.1'
port = 23005

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()
print("Listening...")

while True:
    client_socket, address = server.accept()

    while True:
        client_socket.send("send your user-id".encode("ascii"))
        m = client_socket.recv(1024).decode("ascii")
        unique = True
        for c in clients:
            if c[0] == m:
                unique = False
        if unique:
            print(f"{m} accepted")
            client_socket.send("accepted".encode("ascii"))
            clients.append((m, client_socket))
            break

    thread = threading.Thread(target=handle, args=(client_socket, m,))
    thread.start()
