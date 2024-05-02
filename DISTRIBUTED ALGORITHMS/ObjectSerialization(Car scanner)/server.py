import socket
import pickle

# A class that represents a Serializable object
class Voiture:
    def __init__(self, matricule, couleur):
        self.matricule = matricule
        self.couleur = couleur

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)

    print("Server is running and waiting for connections...")

    client_socket, address = server_socket.accept()

    # Serialize and send an object to the client
    voiture_to_send = Voiture('2345', 'Bleu')
    serialized_data = pickle.dumps(voiture_to_send)
    client_socket.send(serialized_data)

    # Receive and deserialize an object from the client
    received_data = client_socket.recv(1024)
    received_voiture = pickle.loads(received_data)
    print("Received from client:", received_voiture.matricule, received_voiture.couleur)

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    server()
