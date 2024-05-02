import socket
import threading

def receive_messages(client_socket, exit_event):
    try:
        while not exit_event.is_set():
            response = client_socket.recv(1024).decode('utf-8')
            if not response:
                break
            print(response)
    except ConnectionResetError:
        pass  # Handle the connection being reset
    except ConnectionAbortedError:
        pass  # Handle the connection being aborted

    exit_event.set()  # Set the exit event to signal the main thread to exit


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))

    exit_event = threading.Event()

    # Start a separate thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, exit_event))
    receive_thread.start()

    waiting_for_response = False  # Flag to indicate if the client is waiting for a response

    try:
        while True:
            if not waiting_for_response:
                message = input("Enter a message (type '/broadcast' to broadcast, 'exit' to end): ")
            else:
                message = input("Waiting for server response...")

            if message.lower() == 'exit':
                exit_event.set()
                break
            elif message.startswith('/broadcast '):
                client_socket.send(message.encode('utf-8'))
            else:
                client_socket.send(message.encode('utf-8'))
                waiting_for_response = True

    except KeyboardInterrupt:
        pass  # Handle Ctrl+C

    client_socket.close()

if __name__ == "__main__":
    start_client()
