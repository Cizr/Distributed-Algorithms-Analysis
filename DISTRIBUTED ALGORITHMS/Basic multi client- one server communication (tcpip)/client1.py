import socket
import threading

message_lock = threading.Lock()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))

    while True:
        message = input("Enter a message (type 'exit' to end): ")

        with message_lock:
            client_socket.send(message.encode('utf-8'))
            if message.lower() == 'exit':
                break

            # Notify the client that the server is processing
            print("Waiting for server response...")

            response = client_socket.recv(1024).decode('utf-8')
            print("Server response:", response)

    client_socket.close()

if __name__ == "__main__":
    start_client()
