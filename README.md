# Port Management Script

## Overview

This script provides functionality to manage TCP ports on your localhost. It allows you to scan for open ports, open and listen on specific ports, and close those ports when you're done.

## Features

- **Port Scanning:** Check which ports in a specified range are open.
- **Open Port:** Open a specific port and listen for incoming connections.
- **Close Port:** Close a specific port that was previously opened.

## Requirements

- Python 3.x

## Usage

### Scan Ports

```sh
python scanner.py s <hostname> <start_port> <end_port>
```

### Example:
```sh
python scanner.py s localhost 1 500
```

### Open a port:

```sh
  python scanner.py o <hostname> <port>
```
### Example:

```sh
  python scanner.py o localhsot 133
```

### Closing a port:
- **Connect a client to that port first**

### Example:
```sh
  python client.py
  Enter server port<int>: 133
```
- **send close from client and scanner to close that port**

