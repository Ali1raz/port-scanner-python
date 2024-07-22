import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(input("Enter server port<int>: "))
addr = '127.0.0.1'
server_address = (addr, port)

try:
    client.connect(server_address)
    print(f"Connected to the server: ")

    while True:
        message = input("Enter message (type 'close' to exit): ")
        client.sendall(message.encode())

        if message.lower() == 'close':
            break

        data = client.recv(1024)
        print(f"Received from server: {data.decode('utf-8')}")

finally:
    client.close()

