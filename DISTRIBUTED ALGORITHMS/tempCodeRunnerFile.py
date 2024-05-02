import logging
import threading
import time
from queue import Queue
from datetime import datetime
import random

from supervisor import SupervisorThread
from controller_application import ThreadApplicationController

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def simulate_sender(sender_id, receivers, supervisor_queue):
    for receiver_id in receivers:
        message = f"Message from Controller {sender_id} to Controller {receiver_id}"
        logging.info(f"Controller {sender_id} sending: {message}")
        supervisor_queue.put({
            'sender': sender_id,
            'receiver': receiver_id,
            'message': message,
            'timestamp': datetime.now()
        })
        time.sleep(random.uniform(0.1, 1.0)) # Simulate random delay
        
def calculate_node_depth(tree_structure):
    node_depth = {0: 0}  # The root node (Controller 0) is at depth 0
    nodes_to_visit = [(0, 0)]  # Start with the root node

    while nodes_to_visit:
        node, depth = nodes_to_visit.pop()
        for child in tree_structure[node]:
            node_depth[child] = depth + 1
            nodes_to_visit.append((child, depth + 1))

    return node_depth

if __name__ == "__main__":
    random.seed(1)  #Set seed for reproducibility
    #setting a seed ensures that the same sequence of random numbers is produced every time the code is run. 
    supervisor_queue = Queue()
    termination_signal = threading.Event()
    num_controllers = 6  #replace with the actual number of controllers

    #tree structure
    tree_structure = {
        0: [1, 2, 3],  # Controller 0 is the root, with children 1, 2, and 3
        1: [4, 5],     # Controller 1 now has children 4 and 5
        2: [],         # Controller 2 has no children
        3: [],         # Controller 3 has no children
        4: [],         # Controller 4 has no children
        5: []          # Controller 5 has no children
    }

    node_depth = calculate_node_depth(tree_structure)

    supervisor_thread = SupervisorThread(supervisor_queue, termination_signal, num_controllers, node_depth)
    supervisor_thread.start()

    # Create controller threads
    controller_threads = []
    for controller_id in range(num_controllers):
        controller_address = ('localhost', 9000 + controller_id)
        controller_thread = ThreadApplicationController(controller_id, controller_address, supervisor_queue, [(addr, 9000 + addr) for addr in range(num_controllers)], termination_signal)
        controller_threads.append(controller_thread)

    # Start controller threads
    for controller_thread in controller_threads:
        controller_thread.start()

    # Simulate sending messages to the supervisor queue
    sender_threads = []
    for sender_id in range(num_controllers):
        receivers = tree_structure[sender_id]
        sender_thread = threading.Thread(target=simulate_sender, args=(sender_id, receivers, supervisor_queue))
        sender_threads.append(sender_thread)
        sender_thread.start()

    # Simulate some time for threads to execute
    time.sleep(5)

    # Simulate termination
    termination_signal.set()

    # Wait for controller threads to finish
    for sender_thread in sender_threads:
        sender_thread.join()

    for controller_thread in controller_threads:
        controller_thread.join()

    supervisor_thread.join()