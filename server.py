import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 2345

server_socket.bind((host, port))
server_socket.listen(0)

print("ready to connect...")

while True:
    client_socket, address = server_socket.accept()
    sentence = client_socket.recv(1024).decode()

    client_socket.sendall(sentence.upper().encode())
    print(f"got connection from {address}")
    client_socket.close()
    server_socket.close()
