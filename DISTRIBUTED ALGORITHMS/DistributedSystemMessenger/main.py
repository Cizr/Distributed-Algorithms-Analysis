import logging  
import threading  
import time  
from queue import Queue  
from datetime import datetime  
import random  

from supervisor import SupervisorThread  
from controller_application import ThreadApplicationController  


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#simulate sending messages from one controller to another
def simulate_sender(sender_id, receivers, supervisor_queue):
    """
    Simulates the sending of messages from a controller to its receivers.

    Args:
        sender_id (int): The ID of the controller sending the message.
        receivers (list): A list of receiver IDs.
        supervisor_queue (Queue): The queue for communication with the supervisor thread.
    """
    for receiver_id in receivers: #Iterates over each receiver ID in the list of receivers
    
        message = f"Message from Controller {sender_id} to Controller {receiver_id}"
        logging.info(f"Controller {sender_id} sending: {message}")
        #put the message in the supervisor queue (represented as a dictionary)
        supervisor_queue.put({
            'sender': sender_id,
            'receiver': receiver_id,
            'message': message,
            'timestamp': datetime.now()
        })
        #just a random delay before sending the next message
        time.sleep(random.uniform(0.1, 1.0))

# a function to calculate the depth of each node in the topology
def calculate_node_depth(topology):
    """
    Calculates the depth of each node in the given topology using depth-first search (DFS).

    Args:
        topology (dict): The topology represented as a dictionary of nodes and their neighbors.

    Returns:
        dict: A dictionary mapping each node to its depth in the topology.
    """
    node_depth = {}  #dict to store the depth of each node
    visited = set()  #keep track of visited nodes

    def dfs(node, depth):
        """
        Recursive function to perform depth-first search (DFS) traversal.

        Args:
            node: The current node being visited.
            depth: The depth of the current node in the traversal.

        """
        if node in visited:
            return
        visited.add(node)
        node_depth[node] = depth
        for neighbor in topology[node]:
            dfs(neighbor, depth + 1)

    #iterates over each node in each topology 
    for node in topology:
        dfs(node, 0)

    return node_depth  #dictionary mapping nodes to their depths


if __name__ == "__main__":
    random.seed(1)  #making our code predictable and reproducible(same sequence of random delays)

    tree_structure = {
        0: [1, 2, 3],  
        1: [4, 5],     
        2: [],         
        3: [],         
        4: [],         
        5: []          
    }

    ring_structure = {
        0: [1],
        1: [2],
        2: [3],
        3: [0]
    }

    fully_connected_structure = {
        0: [1, 2, 3],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [0, 1, 2]
    }

    print("Select the topology to use:")
    print("1. Tree Topology")
    print("2. Ring Topology")
    print("3. Fully Connected Topology")
    choice = input("Enter your choice (1/2/3): ") 

    if choice == "1":
        topology = tree_structure
    elif choice == "2":
        topology = ring_structure
    elif choice == "3":
        topology = fully_connected_structure
    else:
        print("Invalid choice. Exiting...")  
        exit()

    node_depth = calculate_node_depth(topology) 

    supervisor_queue = Queue()  #Queue for communication between controllers and supervisor
    termination_signal = threading.Event()  #Event instance for signaling termination
    num_controllers = len(topology)  #num of controllers based on the selected topology

    supervisor_thread = SupervisorThread(supervisor_queue, termination_signal, num_controllers, node_depth)
    supervisor_thread.start()  


    controller_threads = []
    for controller_id in range(num_controllers):
        controller_address = ('localhost', 9000 + controller_id)  #define the address for each controller
        controller_thread = ThreadApplicationController(controller_id, controller_address, supervisor_queue, [(addr, 9000 + addr) for addr in range(num_controllers)], termination_signal)
        controller_threads.append(controller_thread)
        controller_thread.start()  

    #sending messages to the supervisor queue
    sender_threads = []
    for sender_id in range(num_controllers):
        receivers = topology[sender_id]
        #Create and start a sender thread
        sender_thread = threading.Thread(target=simulate_sender, args=(sender_id, receivers, supervisor_queue))
        sender_threads.append(sender_thread)
        sender_thread.start()  

    #time for threads to execute
    time.sleep(5)  


    termination_signal.set()  #termination signal to stop the threads
    ''' 
    join() on a thread the program waits at that point until the specified thread finishes its execution.
    '''
    for sender_thread in sender_threads:
        sender_thread.join()  

    for controller_thread in controller_threads:
        controller_thread.join()  


    supervisor_thread.join() 
