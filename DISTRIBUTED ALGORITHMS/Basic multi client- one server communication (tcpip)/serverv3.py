import socket
import threading
import queue
import time

#to create a mutex (mutual exclusion) and ensure synchronized printing to avoid overlapping console output
print_lock = threading.Lock()

#queue so we can store messages from clients
message_queue = queue.Queue()

#stores the active connections with client IDs
client_connections = {}

#just func to handle communication with each connected client
def handle_client(connection, address, client_id):
    #Output connection message when a client connects
    with print_lock:
        print(f"Connected to {client_id} at address: {address}")

    while True:
        #receiving data from the client
        data = connection.recv(1024).decode('utf-8')

        #But we check if data is empty maybe client disconnected
        if not data:
            break

        #output received message from the client
        with print_lock:
            print(f"Received from {client_id}: {data}")

        #the received message will be along with client_id into the message queue
        message_queue.put((client_id, data))

    #if client disconnects close
    connection.close()

    #remove client IDs connection from the dictionary
    with print_lock:
        print(f"Connection with {client_id} closed.")
        del client_connections[client_id]

#func to process messages 
def process_messages():
    while True:
        #first we check if the message queue is not empty
        if not message_queue.empty():
            with print_lock:
                #getting the client_id and message from the message queue
                client_id, message = message_queue.get()

                #entering a response for the client
                response = input(f"Enter your response for {client_id}: ")

                #another output response
                print(f"Response to {client_id}: {response}")

                #checking if the client is still connected
                if client_id in client_connections:
                    #we send the response back to the client
                    client_connections[client_id].send(response.encode('utf-8'))

                #1sec delay to handle safety
                time.sleep(1)

#func to start the server
def start_server():
    #socket for server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Binding the socket to a specific address and port
    server_socket.bind(('localhost', 8888))

    #listening for incoming connections (5 clients in the queue)
    server_socket.listen(5)

    #showing that the server is running
    with print_lock:
        print("Server is running and waiting for connections...")

    #used to assign unique client IDs to each connected client
    client_counter = 1

    try:
        #"process_messages" function runs in a separate thread process messages from clients
        #The use of a daemon thread ensures that the thread terminates when the server program exits
        threading.Thread(target=process_messages, daemon=True).start()

        while True:
            #accepting new connection from a client
            connection, address = server_socket.accept()

            #generating a unique client ID
            client_id = f"Client {client_counter}"
            client_counter += 1

            #storing the client connection in the dictionary
            client_connections[client_id] = connection

            #to handle communication with the client start a new thread
            client_thread = threading.Thread(target=handle_client, args=(connection, address, client_id))
            client_thread.start()

    except KeyboardInterrupt:
        #keyboard interrupt
        with print_lock:
            print("Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
