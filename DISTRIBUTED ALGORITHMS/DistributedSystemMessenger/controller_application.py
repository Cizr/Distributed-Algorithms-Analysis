import logging  
import socket  
import threading  
from queue import Queue  
from enum import Enum  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
'''
Configures the logging system to display messages with INFO level or higher in the format:
[timestamp] - [log level] - [message]
'''

class ControllerState(Enum):
    '''
    Defines an enumeration class for controller states.
    '''
    INITIATOR = "INITIATOR"  
    IDLE = "IDLE"  
    DONE = "DONE"  

class ThreadApplicationController(threading.Thread):
    '''
    Represents a thread-based application controller.
    '''
    def __init__(self, controller_id, controller_address, supervisor_queue, all_controller_addresses, termination_signal):
        '''
        Initializes the ThreadApplicationController object.

        Args:
            controller_id (int): The ID of the controller.
            controller_address (tuple): The address (host, port) of the controller.
            supervisor_queue (Queue): The queue for communication with the supervisor thread.
            all_controller_addresses (list): List of addresses of all controllers.
            termination_signal (threading.Event): Signal to indicate termination of the thread.
        '''
        super().__init__() 
        self.controller_id = controller_id  
        self.controller_address = controller_address  
        self.supervisor_queue = supervisor_queue  
        self.all_controller_addresses = all_controller_addresses  
        self.termination_signal = termination_signal  
        self.state = ControllerState.IDLE  
        self.send_socket = None  
        self.initialize_socket()  

    def initialize_socket(self):
        '''
        Initializes the send socket for communication.
        '''
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, event):
        '''
        Sends a message to all controllers.

        Args:
            event (str): The event message to be sent.
        '''
        if not self.send_socket:
            self.initialize_socket()  #Initialize the socket if not already initialized
        for receiver in self.all_controller_addresses:
            try:
                self.send_socket.connect(receiver)  #Connect to the receiver
                self.send_socket.sendall(event.encode())  # Send the event message
            except ConnectionError as ce:
                logging.error(f"Error connecting to {receiver}: {ce}")  
            finally:
                if self.send_socket:
                    self.send_socket.close()  #Close the socket after sending message
                    self.send_socket = None

    def process_event(self, event):
        '''
        Processes an incoming event based on the controller state.

        Args:
            event (str): The event received by the controller.
        '''
        if self.state == ControllerState.INITIATOR and event == "I":
            logging.info(f"Controller {self.controller_id} initiated flooding.")  
            self.state = ControllerState.DONE  #controller state to DONE
            self.send_message("I")  #initiation message to all controllers
        elif self.state == ControllerState.IDLE and event.startswith("RECEIVING"):
            logging.info(f"Controller {self.controller_id} received a message.")  
            self.state = ControllerState.DONE  #controller state to DONE
            self.send_message("I")  #initiation message to all controllers

    def run(self):
        '''
        Runs the controller thread, handling incoming events and processing them.
        '''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(self.controller_address)  
            server_socket.listen()  

            while not self.termination_signal.is_set():  
                try:
                    client_socket, _ = server_socket.accept()  #accepting incoming connections from other controllers
                    with client_socket:  #automatically close the socket
                        event_data = client_socket.recv(1024)  #event data from the client socket
                        if not event_data:
                            continue  
                        event = event_data.decode()  #decoding the received data to get the event message

                        #process the event based on the flooding algorithm logic
                        self.process_event(event)

                        #sending information to the Supervisor Thread
                        info_for_supervisor = f"Controller {self.controller_id} processed Event: {event}"
                        self.supervisor_queue.put(info_for_supervisor)

                        #Log the messages sent by the controller
                        logging.info(f"Controller {self.controller_id} sent message: {event}")
                except ConnectionError as ce:
                    logging.error(f"Connection error occurred: {ce}")  
                except Exception as e:
                    logging.error(f"Unexpected error occurred: {e}")  

        logging.info(f"Controller {self.controller_id} terminated.")  



'''
Initializes the controller object with necessary attributes such as ID, address, queue for communication with the supervisor thread, addresses of all controllers, and termination signal.
Also initializes the send socket for communication.
Methods:
initialize_socket(): Initializes the send socket.
send_message(event): Sends a message to all controllers.
process_event(event): Processes an incoming event based on the controller's state.
run(): Runs the controller thread, handling incoming events, processing them, and logging the messages sent by the controller.
'''

'''
Main Program:
    It creates instances of the ThreadApplicationController class for each controller, initializes their threads, and starts their execution.
    It simulates sending messages to the supervisor queue using sender threads.
    It waits for all sender and controller threads to finish their execution using join() method.
    it waits for the supervisor thread to finish before terminating the program.
'''