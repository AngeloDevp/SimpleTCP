import socket
import threading

HOST = "127.0.0.1"
PORT = 9999
BYTES = 1024
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nickname = input("Choose a nickname: ")

def ReceiveMessages():
    while True:
        try:
            message = client.recv(BYTES).decode(FORMAT)
            if message == "NICKNAME:":
                client.send(nickname.encode(FORMAT))
            else:
                print(message)
        except:
            print("Connection Error")
            client.close()
            break

def SendMessages():
    while True:
        message = f"{nickname}: {input("")}"
        # print(f"FLAG 5: Something bad happens with client: {client}")

        client.send(message.encode(FORMAT))

ReceiveMessagesThread = threading.Thread(target=ReceiveMessages)
ReceiveMessagesThread.start()

SendMessagesThread = threading.Thread(target=SendMessages)
SendMessagesThread.start()