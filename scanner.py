import socket
import sys
import threading

open_sockets = {}

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((host, port))
        sock.close()
        print(f"Port {port} is open")
        return True
    except socket.error:
        return False


def scan_ports(hostname, start, end):
    threads = []
    results = []

    def thread_target(host, port):
        if scan_port(host, port):
            results.append(port)

    for port in range(start, end + 1):
        # Use threading for concurrency and multiple tasks at a time
        thread = threading.Thread(target=thread_target, args=(hostname, port))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    if results:
        print(f"Open ports: {sorted(results)}")
    else:
        print("No open ports found")


def open_port(hostname, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (hostname, port)
        sock.bind(server_address)
        sock.listen(1)
        print(f"Port {port} is now open and listening for connections on {hostname}")
        open_sockets[port] = sock
        print(f"Current open sockets: {list(open_sockets.keys())}")
        return sock
    except Exception as e:
        print(f"Failed to open port {port}: {e}")
        return None


def close_port(port):
    print(f"Attempting to close port {port}")
    if port in open_sockets:
        try:
            open_sockets[port].close()
            del open_sockets[port]
            print(f"Port {port} is now closed")
        except Exception as e:
            print(f"Failed to close port {port}: {e}")
    else:
        print(f"Port {port} is not managed by this program")
    print(f"Current open sockets after closing: {list(open_sockets.keys())}")


def handle_client(sock):
    try:
        while True:
            connection, client_address = sock.accept()
            try:
                print(f"Connection from {client_address}")
                while True:
                    data = connection.recv(1024)
                    if not data:
                        print("No more data from", client_address)
                        break
                    print("----\nReceived from client:", data.decode())
                    reply = input("<close> to exit, Enter reply: ")
                    connection.sendall(reply.encode())
                    if reply.lower() == 'close':
                        break
            finally:
                connection.close()
            # Stop handling clients after the connection is closed
            if sock in open_sockets.values():
                close_port(sock.getsockname()[1])
                break
    except KeyboardInterrupt:
        print("Server interrupted by user")
    finally:
        sock.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python [file].py <option> [hostname] [start_port] [end_port]/[port]")
        sys.exit(1)

    option = sys.argv[1]

    if option == 's':
        if len(sys.argv) != 5:
            print("Usage: python [file].py s <hostname> <start_port> <end_port>")
            sys.exit(1)

        hostname = sys.argv[2]
        try:
            start = int(sys.argv[3])
            end = int(sys.argv[4])
        except ValueError:
            print("Error: start and end ports must be integers")
            sys.exit(1)

        if start < 1 or end > 65535:
            print("Error: ports must be in range 1-65535")
            sys.exit(1)
        if start > end:
            print("Error: start_port must be <= end_port")
            sys.exit(1)

        scan_ports(hostname, start, end)

    elif option == 'o':
        if len(sys.argv) != 4:
            print("Usage: python [file].py o <hostname> <port>")
            sys.exit(1)

        hostname = sys.argv[2]
        try:
            port = int(sys.argv[3])
        except ValueError:
            print("Error: port must be an integer")
            sys.exit(1)

        if port < 1 or port > 65535:
            print("Error: port must be in range 1-65535")
            sys.exit(1)

        sock = open_port(hostname, port)
        if not sock:
            sys.exit(1)

        handle_client(sock)

    elif option == 'c':
        if len(sys.argv) != 3:
            print("Usage: python [file].py c <port>")
            sys.exit(1)

        try:
            port = int(sys.argv[2])
        except ValueError:
            print("Error: port must be an integer")
            sys.exit(1)

        if port < 1 or port > 65535:
            print("Error: port must be in range 1-65535")
            sys.exit(1)

        close_port(port)

    else:
        print("Error: unknown option. Use 's' to scan ports, 'o' to open a port, or 'c' to close a port.")
        sys.exit(1)


if __name__ == "__main__":
    main()
