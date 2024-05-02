import socket
import threading

def handle_client(client_socket, client_address):
    try:
        while True:
            # Receive data from the client in chunks of 1024 bytes
            data = client_socket.recv(1024)
            # If no more data is received, break out of the loop
            if not data:
                break

            # Decode the received data to a UTF-8 string and print it on the server side
            command = data.decode('utf-8')
            print(f"Received from {client_address}: {command}")

            # If the client sends 'exit', break out of the loop and close the connection
            if command.lower() == "exit":
                break

            try:
                # If the received command is a valid integer, double it and send back to the client
                number = int(command)
                result = number * 2
                client_socket.send(str(result).encode('utf-8'))
            except ValueError:
                # If the conversion to integer fails, send an error message to the client
                client_socket.send("Invalid input. Please enter a valid number or type 'exit' to quit.".encode('utf-8'))

    except Exception as e:
        # Catch any unexpected exceptions during communication and print for debugging
        print(f"Error handling client {client_address}: {str(e)}")
    finally:
        # Print a message about closing the connection and close the client socket
        print(f"Closing connection from {client_address}")
        client_socket.close()

def start_server():
    # Create a socket for the server with IPv4 address family and TCP socket type
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the server socket to the address ('127.0.0.1', 12345)
    server_socket.bind(('127.0.0.1', 12345))
    # Allow up to 5 queued connections
    server_socket.listen(5)
    # Print a message indicating that the server is listening
    print("Server listening on port 12345")

    try:
        while True:
            # Accept an incoming connection and get the client socket and address
            client_socket, client_address = server_socket.accept()
            # Print a message about the accepted connection
            print(f"Accepted connection from {client_address}")

            # Create a new thread for handling communication with the connected client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            # Start the thread to handle the client
            client_thread.start()

    except KeyboardInterrupt:
        # Handle a keyboard interrupt (Ctrl+C) to gracefully shut down the server
        print("Server shutting down.")
    finally:
        # Close the server socket in the finally block to ensure cleanup
        server_socket.close()

# Main entry point
if __name__ == "__main__":
    # Call the start_server function to initiate the server
    start_server()
