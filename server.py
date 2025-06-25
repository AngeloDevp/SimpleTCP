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

def RealPassword():
    with open("ADMINPASSWORD.txt", "r") as f:
        PASSWORD = f.read().strip()
    return PASSWORD 

def Broadcast(message):
    for clientDic in listOfClients:
        for nickname in clientDic:
            # print(f"FLAG 4: Verify who is sending, must be a socket: {clientDic[nickname]}")
            clientDic[nickname].send(message.encode(FORMAT))

def KickUser(nameToKick):
    try:
        removed = RemoveClient(nameToKick)
        if removed:
            print(f"{nameToKick} removed from the chat!")
            socketToClose = GetSocket(nameToKick)
            socketToClose.close()
            Broadcast(f"{nameToKick} was kicked by an admin")

    except:
        print("Something wrong happend")

def BanUser(nameToBan):
    
    KickUser(nameToBan)

    with open("banslist.txt", "a") as f:
        f.write(f"{nameToBan}\n")

def HandleMessage(client, nickname):
    while True:
        try:
            msg = message = client.recv(BYTES).decode(FORMAT)
            msgSlice = msg.slice(" ")
            nameToApplyAction = msgSlice[1]
            
            if msg.startswith("/kick"):
                KickUser(nameToApplyAction)

            elif msg.startswith("/ban"):
                BanUser(nameToApplyAction)
                print(f"{nameToApplyAction} banned!")
            else:
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
                return True

def GetSocket(nicknameToFind):
    for clientDic in listOfClients:
        for nickname, socket in clientDic:
            if nickname == nicknameToFind:
                print(f"FLAG 1: SOCKET = {socket}")
                return socket
            

def ReceiveConnection():
    while True:
        client, address = server.accept()

        client.send("NICKNAME:".encode(FORMAT))
        nickname = client.recv(BYTES).decode(FORMAT)

        if nickname == "admin":
            client.send("PASSWORD".encode(FORMAT))
            passwordClient = client.recv(BYTES).decode(FORMAT)
            PASSWORD = RealPassword()

            if passwordClient == PASSWORD:
                client.send("ACCEPTED".encode(FORMAT))
            else:
                client.send("REFUSED".encode(FORMAT))
                client.close()
                continue
        
        nickNameClient = {nickname: client}
        listOfClients.append(nickNameClient)
        
        Broadcast(f"{nickname} join the chat")
        client.send("Connected successfully".encode(FORMAT))

        serverThread = threading.Thread(target=HandleMessage, args=(client, nickname))
        serverThread.start()

print("Waiting for connection")
ReceiveConnection()



        




