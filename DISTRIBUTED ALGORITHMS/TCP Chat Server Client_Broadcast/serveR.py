
import socket
import threading
import queue
import time
import signal
import sys

# Creating a lock for thread-safe printing
print_lock = threading.Lock()

# Using a queue to store messages for further processing
message_queue = queue.Queue()

# Dictionary to store client connections
client_connections = {}

# Flag to control the server running state
server_running = True

# Function to handle client connections
def handle_client(connection, address, client_id):
    with print_lock:
        print(f"Connected to {client_id} at address: {address}")

    try:
        # Continuously receive and process data from the client
        while True:
            data = connection.recv(1024).decode('utf-8')
            if not data:
                break

            with print_lock:
                print(f"Received from {client_id}: {data}")

            # Check if it's a broadcast message
            if data.startswith("/broadcast "):
                broadcast_message = data[len("/broadcast "):]
                
                # Iterate through all connected clients and send the broadcast message
                for other_client_id, other_connection in client_connections.items():
                    if other_client_id != client_id:
                        other_connection.send(f"[Broadcast] {client_id}: {broadcast_message}".encode('utf-8'))
            else:
                # Regular message handling
                response = input(f"Enter your response for {client_id}: ")
                print(f"Response to {client_id}: {response}")

                # Send a response to the client
                if client_id in client_connections:
                    client_connections[client_id].send(f"SERVER RESPONSE: {response}\nEnter a message: ".encode('utf-8'))

    except Exception as e:
        print(f"Error in client {client_id}: {e}")

    # Close the connection and remove the client from the dictionary
    connection.close()
    with print_lock:
        print(f"Connection with {client_id} closed.")
        del client_connections[client_id]

# Function to process messages from the queue
def process_messages():
    while True:
        if not message_queue.empty():
            with print_lock:
                client_id, message = message_queue.get()
                response = input(f"Enter your response for {client_id}: ")
                print(f"Response to {client_id}: {response}")

                # Send a response to the client
                if client_id in client_connections:
                    client_connections[client_id].send(f"SERVER RESPONSE: {response}\nEnter a message: ".encode('utf-8'))

                # Introduce a delay to avoid rapid message processing
                time.sleep(1)

# Function to handle server shutdown
def shutdown_server(signum, frame):
    global server_running
    server_running = False

    # Notify connected clients about server shutdown
    for client_connection in client_connections.values():
        try:
            client_connection.send("SERVER SHUTDOWN".encode('utf-8'))
        except:
            pass  # Handle exceptions when sending to clients

    # Exit the program
    sys.exit(0)

# Set up a signal handler for graceful shutdown on SIGINT (Ctrl+C)
if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_server)

    # Set up server socket and start listening for connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8888))
    server_socket.listen(5)

    print("Server is running and waiting for connections...")

    # Counter for assigning client IDs
    client_counter = 1

    try:
        # Start a thread for processing messages
        threading.Thread(target=process_messages, daemon=True).start()

        # Main loop to accept client connections
        while server_running:
            connection, address = server_socket.accept()
            client_id = f"Client {client_counter}"
            client_counter += 1
            client_connections[client_id] = connection

            # Start a thread to handle the new client connection
            client_thread = threading.Thread(target=handle_client, args=(connection, address, client_id))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        # Close the server socket when done
        server_socket.close()
