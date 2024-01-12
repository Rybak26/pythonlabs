import socket
import threading
import time

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Клієнт говорить: {data}")
            print(f"Час отримання: {time.strftime('%H:%M:%S')}")

            if data.lower() == "завершити":
                print("Завершення з'єднання з клієнтом")
                break
        except Exception as e:
            print(f"Помилка обробки даних від клієнта: {e}")
            break

    client_socket.close()

server_ip = '127.0.0.1'
server_port = 4321

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print(f"Сервер слухає на {server_ip}:{server_port}")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Новий клієнт підключився: {client_address}")

        # Запуск окремого потоку для обробки клієнта
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

except KeyboardInterrupt:
    print("Сервер було відключено користувачем.")

finally:
    server_socket.close()