import socket

server_ip = '127.0.0.1'
server_port = 4321

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_ip, server_port))
    print(f"Connected to the server {server_ip}:{server_port}")

    while True:
        user_input = input("Client 2, enter text for the server (or 'exit' to quit): ")
        client_socket.send(user_input.encode('utf-8'))

        if user_input.lower() == 'exit':
            break

except ConnectionRefusedError:
    print(f"Connection error: Server {server_ip}:{server_port} is not available.")

finally:
    client_socket.close()
