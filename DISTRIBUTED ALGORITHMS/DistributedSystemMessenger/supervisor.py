import threading  
from queue import Queue, Empty  
import time  
from datetime import datetime  
import socket  

class SupervisorThread(threading.Thread):
    ''' 
    This class represents the supervisor thread responsible for coordinating controller activities.
    '''

    message_count = 0  #counter to count the number of messages
    max_unit_time = 0  #shared variable to store the maximum unit time
    lock = threading.Lock()  #thread-safe counter increment
    start_signal_received = False  #Flag to indicate if the start signal is received

    def __init__(self, supervisor_queue, termination_signal, num_controllers, node_depth):
        '''
        Initializes the SupervisorThread object.

        Args:
            supervisor_queue (Queue): The queue for communication with the controller threads.
            termination_signal (threading.Event): Signal to indicate termination of the thread.
            num_controllers (int): Number of controller threads.
            node_depth (dict): Dictionary mapping each node to its depth in the topology.
        '''
        super().__init__()  
        self.supervisor_queue = supervisor_queue  
        self.termination_signal = termination_signal  
        self.num_controllers = num_controllers 
        self.node_depth = node_depth  
        self.start_time = None  

    def run(self):
        ''' 
        Runs the SupervisorThread. Handles incoming controller connections and communication.
        '''
        #creating a server socket to listen for controller connections
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 8888))  
        server_socket.listen(self.num_controllers)  

        #accepting incoming connections and handling them in separate threads
        while not self.termination_signal.is_set():  #Continue until termination signal is set
            client_socket, _ = server_socket.accept()  #Accepting a new controller connection
            print("Controller connected:", client_socket.getpeername())  
            threading.Thread(target=self.handle_controller, args=(client_socket,)).start()  

    def handle_controller(self, client_socket):
        ''' 
        Handles communication with a controller until the start signal is received or an error occurs.

        Args:
            client_socket (socket.socket): The socket object for communication with the controller.
        '''
        try:
            while not self.start_signal_received:  #until the start signal is received
                data = client_socket.recv(1024).decode()  
                if data == "/start":  
                    self.start_signal_received = True  
                    self.start_time = datetime.now()  
                    break  
        except Exception as e:  
            print("Error handling controller:", e)  
        finally:
            client_socket.close()  
            print("Controller disconnected")  

    def start_broadcast(self):
        ''' 
        Starts broadcasting messages to controller threads.
        '''
        print("Broadcast started!")  
        self.start()  

    message_count = 0  
    max_unit_time = 0  
    lock = threading.Lock()  

    def __init__(self, supervisor_queue, termination_signal, num_controllers, node_depth):
        '''
        Initializes the SupervisorThread object.

        Args:
            supervisor_queue (Queue): The queue for communication with the controller threads.
            termination_signal (threading.Event): Signal to indicate termination of the thread.
            num_controllers (int): Number of controller threads.
            node_depth (dict): Dictionary mapping each node to its depth in the topology.
        '''
        super().__init__()  
        self.supervisor_queue = supervisor_queue  
        self.termination_signal = termination_signal  
        self.num_controllers = num_controllers  
        self.node_depth = node_depth  
        self.start_time = datetime.now()  

    def run(self):
        ''' 
        Runs the SupervisorThread. Processes messages from the supervisor queue and prints summary.
        '''
        while not self.termination_signal.is_set() or not self.supervisor_queue.empty():
            try:
                summary = self.supervisor_queue.get(timeout=1)  #Getting a summary from the supervisor queue
                with self.lock:  #Acquiring the lock for thread-safe counter increment
                    self.message_count += 1  
                    self.max_unit_time = max(self.max_unit_time, self.node_depth[summary['receiver']])  
                unit_time = self.node_depth[summary['receiver']]  
                elapsed_time = datetime.now() - self.start_time  
                real_time = elapsed_time.total_seconds()  
                
               
                print("=" * 50)
                print(f"Supervisor Summary: {summary}")
                print(f"Messages exchanged: {self.message_count}")
                print(f"Unit time: {unit_time}")  
                print(f"Real time: {real_time} seconds")
            except Empty:  
                pass  

        print("=" * 50)
        print(f"Supervisor Thread terminated.")
        print(f"Total Messages: {self.message_count}")
        print(f"Total unit of time: {self.max_unit_time}")



'''
First Occurrence:
      initially defined as a class variable outside any method. This means it's a shared variable among all instances of SupervisorThread 
      and can be accessed using SupervisorThread.message_count.
      
Second Occurrence:
    defined again but as an instance variable using self.message_count.
    incremented each time a message is processed by the supervisor thread instance running this method.
   per-instance counter to track the number of messages processed by each individual supervisor thread.
'''