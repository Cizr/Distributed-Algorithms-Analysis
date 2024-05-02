import socket

def send_number_to_server(number):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))
    
    while True:
        client_socket.send(str(number).encode('utf-8'))

        data = client_socket.recv(1024)
        result = data.decode('utf-8')
        print(f"Server response: {result}")

        user_input = input("Enter a number or type 'exit' to quit: ")
        if user_input.lower() == 'exit':
            break

        try:
            number = int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    client_socket.close()

if __name__ == "__main__":
    user_input = input("Enter a number: ")
    try:
        number = int(user_input)
        send_number_to_server(number)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
