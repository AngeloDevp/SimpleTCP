import socket
import threading

HOST = "127.0.0.1"
PORT = 9999
FORMAT = "utf-8"
BYTES = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

listOfClients = []

def Broadcast(message):
    for clientDic in listOfClients:
        for nickname in clientDic:
            # print(f"FLAG 4: Verify who is sending, must be a socket: {clientDic[nickname]}")
            clientDic[nickname].send(message.encode(FORMAT))

def HandleMessage(client, nickname):
    while True:
        try:
            message = client.recv(BYTES).decode(FORMAT)
            # print(f"FLAG 6: Review the message from HandleMessage {message}")
            Broadcast(message)
        except:
            RemoveClient(nickname)
            client.close()
            Broadcast("Somebody left the chat")
            break

def RemoveClient(nickname):
    for clientDic in listOfClients:
        for nicknameDic in clientDic:
            if nicknameDic == nickname: 
                listOfClients.remove(clientDic)

def ReceiveConnection():
    while True:
        client, address = server.accept()
        # print(f"FLAG 1: Client: {client}, Address: {address} connected")
        
        client.send("NICKNAME:".encode(FORMAT))
        nickname = client.recv(BYTES).decode(FORMAT)

        # print(f"FLAG 3: Nickname Received: {nickname}")

        nickNameClient = {nickname: client}
        listOfClients.append(nickNameClient)
        # print(f"FLAG 2: Clients List {listOfClients}")

        Broadcast(f"{nickname} join the chat")
        client.send("Connected successfully".encode(FORMAT))

        serverThread = threading.Thread(target=HandleMessage, args=(client, nickname))
        serverThread.start()

print("Waiting for connection")
ReceiveConnection()



        




