import socket
import threading

HOST = "127.0.0.1"
PORT = 9999
BYTES = 1024
FORMAT = "utf-8"
COMMANDS = ["/kick", "/ban"]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nickname = input("Choose a nickname: ")
if nickname == "admin":
    passwordClient = input("Write your password: ").strip()

stopThread = False

def ReceiveMessages():
    while True:

        global stopThread

        if stopThread:
            break

        try:
            message = client.recv(BYTES).decode(FORMAT)
            if message == "NICKNAME:":
                client.send(nickname.encode(FORMAT))
                if nickname == "admin":
                    requestPassword = client.recv(BYTES).decode(FORMAT)
                    if requestPassword == "PASSWORD":
                        client.send(passwordClient.encode(FORMAT))
                        response = client.recv(BYTES).decode(FORMAT)
                        if response != "REFUSE":
                            print("connected")
                        else:
                            stopThread = True
            else:
                print(message)
        except:
            print("Connection Error")
            client.close()
            break

def SendMessages():
    while True:
        
        if stopThread:
            break        
        
        message = f"{nickname}: {input("")}".lower()

        if message[len(nickname)+2].startswith("/"):
            if nickname == "admin":
                for i in COMMANDS:
                    if i in message:
                        messageSplit = message.split(" ")
                        action = messageSplit[1]
                        name = messageSplit[2]
                        client.send(f"{action} {name}".encode(FORMAT))
            else:
                print("Permission denied!")         
        else:
            client.send(message.encode(FORMAT))

ReceiveMessagesThread = threading.Thread(target=ReceiveMessages, )
ReceiveMessagesThread.start()

SendMessagesThread = threading.Thread(target=SendMessages)
SendMessagesThread.start()