import socket
import pickle

# A class that represents a Serializable object
class Voiture:
    def __init__(self, matricule, couleur):
        self.matricule = matricule
        self.couleur = couleur

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    # Receive and deserialize an object from the server
    received_data = client_socket.recv(1024)
    received_voiture = pickle.loads(received_data)
    print("Received from server:", received_voiture.matricule, received_voiture.couleur)

    # Serialize and send an object to the server
    voiture_to_send = Voiture('6789', 'Rouge')
    serialized_data = pickle.dumps(voiture_to_send)
    client_socket.send(serialized_data)

    client_socket.close()

if __name__ == "__main__":
    client()


#pickle.dumps(voiture_to_send) was used to serialize the Voiture object before sending it over the network, 
#and pickle.loads(received_data) was used on the receiving side to deserialize the received byte stream back into a Voiture object.
#This allows for the easy transmission of complex objects between different Python processes or over a network.