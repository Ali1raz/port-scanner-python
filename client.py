import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 2345

client_socket.connect((host, port))
sentence = input("enter lowercase: ")

client_socket.sendall(sentence.encode())
response = client_socket.recv(1024).decode()

print("from server: ", response)
client_socket.close()