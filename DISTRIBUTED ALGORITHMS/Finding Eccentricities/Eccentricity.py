from mpi4py import MPI

# Constants
ROOT = 0
NR_NODES = 6
TRUE = 1
FALSE = 0

# The status of the node
class STATUS_ENUM:
    AVAILABLE = 0
    ACTIVE = 1
    PROCESSING = 2
    DONE = 3

# The type of the message that is sent to neighbors
class MESSAGE_TYPE:
    ACTIVATE = 0
    SATURATION = 1
    RESOLUTION = 2

def Initialize(dist, np):
    """
    Initializes the distances vector with zeros.

    Args:
        dist (list): The distances vector to initialize.
        np (int): The number of processes.
    """
    for i in range(np):
        dist[i] = 0

def Prepare_Message(dist, np):
    """
    Prepares a message value by computing the maximum distance from neighbors.

    Args:
        dist (list): The distances vector.
        np (int): The number of processes.

    Returns:
        int: The prepared message value.
    """
    maxdist = max(dist)
    return maxdist + 1

def Process_Message(dist, received_distance, sender):
    """
    Updates the distances vector with the received distance from a sender.

    Args:
        dist (list): The distances vector.
        received_distance (int): The distance received from the sender.
        sender (int): The ID of the sender.
    """
    dist[sender] = received_distance

def Calculate_Eccentricities(dist, np):
    """
    Calculates the eccentricity of a node.

    Args:
        dist (list): The distances vector.
        np (int): The number of processes.

    Returns:
        int: The calculated eccentricity.
    """
    return max(dist)

def Resolve(dist, nodes, received_distance, my_rank, parent, sender, np, request):
    """
    Enters the resolution stage for saturated nodes.

    Args:
        dist (list): The distances vector.
        nodes (list): The adjacency matrix representing the graph.
        received_distance (int): The distance received from the sender.
        my_rank (int): The ID of the current process.
        parent (int): The parent ID.
        sender (int): The ID of the sender.
        np (int): The number of processes.
        request (MPI.Request): The MPI request parameter.

    Returns:
        int: The eccentricity of the node.
    """
    Process_Message(dist, received_distance, sender)
    eccentricity = Calculate_Eccentricities(dist, np)

    for dest in range(np):
        if nodes[my_rank][dest] != 0 and dest != parent:
            maxdist = max(dist[i] for i in range(np) if i != dest)
            message = maxdist + 1
            request.send(message, dest=dest, tag=MESSAGE_TYPE.RESOLUTION)

    return eccentricity

def Print_vector(v):
    """
    Displays a vector to the console.

    Args:
        v (list): The vector to print.
    """
    print("V =", v)

def main():
    """
    The main function for all the processes.
    """
    comm = MPI.COMM_WORLD
    my_rank = comm.Get_rank()
    nr_processes = comm.Get_size()
    status = MPI.Status()
    request = MPI.Request()

    # The adjacency matrix representing the graph
    nodes = [
        [0, 1, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0]
    ]

    # Variables initialization
    distances = [0] * NR_NODES
    node_status = STATUS_ENUM.AVAILABLE
    parent = -1
    nr_neighbors = sum(1 for i in range(nr_processes) if nodes[my_rank][i])
    temp_nr_neighbors = nr_neighbors
    finished = FALSE
    eccentricity = -1
    neighbors_sum = sum(i for i in range(nr_processes) if nodes[my_rank][i])

    # Main loop
    while not finished:
        # ACTIVATION state
        if node_status == STATUS_ENUM.AVAILABLE:
            if my_rank == ROOT:
                for dest in range(nr_processes):
                    if nodes[my_rank][dest]:
                        comm.isend(0, dest=dest, tag=MESSAGE_TYPE.ACTIVATE)

                Initialize(distances, nr_processes)
                if nr_neighbors == 1:
                    for dest in range(nr_processes):
                        if nodes[my_rank][dest]:
                            parent = dest

                    message = Prepare_Message(distances, nr_processes)
                    comm.isend(message, dest=parent, tag=MESSAGE_TYPE.SATURATION)
                    node_status = STATUS_ENUM.PROCESSING
                else:
                    node_status = STATUS_ENUM.ACTIVE
            else:
                message = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
                source = status.Get_source()
                tag = status.Get_tag()

                if tag == MESSAGE_TYPE.ACTIVATE:
                    for dest in range(nr_processes):
                        if nodes[my_rank][dest] and dest != source:
                            comm.isend(0, dest=dest, tag=MESSAGE_TYPE.ACTIVATE)

                    Initialize(distances, nr_processes)
                    if nr_neighbors == 1:
                        parent = source
                        message = Prepare_Message(distances, nr_processes)
                        comm.isend(message, dest=parent, tag=MESSAGE_TYPE.SATURATION)
                        node_status = STATUS_ENUM.PROCESSING
                    else:
                        node_status = STATUS_ENUM.ACTIVE

        # ACTIVE STAGE
        elif node_status == STATUS_ENUM.ACTIVE:
            message = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            source = status.Get_source()
            tag = status.Get_tag()

            if tag == MESSAGE_TYPE.SATURATION:
                temp_nr_neighbors -= 1
                neighbors_sum -= source

                Process_Message(distances, message, source)
                if temp_nr_neighbors == 1:
                    message = Prepare_Message(distances, nr_processes)
                    parent = neighbors_sum
                    comm.isend(message, dest=parent, tag=MESSAGE_TYPE.SATURATION)
                    node_status = STATUS_ENUM.PROCESSING

        # PROCESSING STAGE
        elif node_status == STATUS_ENUM.PROCESSING:
            message = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            source = status.Get_source()
            tag = status.Get_tag()

            if tag == MESSAGE_TYPE.SATURATION:
                eccentricity = Resolve(distances, nodes, message, my_rank, parent, source, nr_processes, request)
                message = eccentricity
                comm.isend(message, dest=parent, tag=MESSAGE_TYPE.RESOLUTION)
                node_status = STATUS_ENUM.DONE
            elif tag == MESSAGE_TYPE.RESOLUTION:
                eccentricity = Resolve(distances, nodes, message, my_rank, parent, source, nr_processes, request)
                node_status = STATUS_ENUM.DONE

        # DONE State
        elif node_status == STATUS_ENUM.DONE:
            print("r({}) = {}".format(my_rank, eccentricity))
            finished = TRUE

    comm.barrier()  # Ensure all processes finish before finalizing MPI
    MPI.Finalize()

if __name__ == "__main__":
    main()

'''

# Output
[0] AVAILABLE and sending ACTIVATION to neighbors
[0] AVAILABLE and sending SATURATION to 1
[1] AVAILABLE and receiving ACTIVATION from 0
[2] AVAILABLE and receiving ACTIVATION from 1
[2] AVAILABLE and sending SATURATION to 1
[2] PROCESSING from 1 and sending RESOLUTION to neighbors
r(2) = 3
[3] AVAILABLE and receiving ACTIVATION from 1
[3] ACTIVE and receiving SATURATION from 1
[3] ACTIVE and receiving SATURATION from 5
[3] ACTIVE and sending SATURATION to 5
[4] AVAILABLE and receiving ACTIVATION from 1
[4] AVAILABLE and sending SATURATION to 1
[4] SATURATED from 1 and sending RESOLUTION to parent
r(4) = 2
[5] AVAILABLE and receiving ACTIVATION from 3
[5] AVAILABLE and sending SATURATION to 3
[1] ACTIVE and receiving SATURATION from 0
[1] ACTIVE and receiving SATURATION from 2
[1] ACTIVE and receiving SATURATION from 4
[1] ACTIVE and sending SATURATION to 4
[1] PROCESSING from 4 and sending RESOLUTION to neighbors
r(1) = 2
[0] PROCESSING from 1 and sending RESOLUTION to neighbors
r(0) = 3
[5] SATURATED from 3 and sending RESOLUTION to parent
r(5) = 2
15
[3] PROCESSING from 5 and sending RESOLUTION to neighbors
r(3) = 2
'''


'''
Activation Phase:
    Process 0 sends activation messages to its neighbors.
    Process 0 sends a saturation message to Process 1.
    
Activation and Saturation Phase:
    Process 1 receives activation messages from Process 0 and Process 2.
    Process 2 receives an activation message from Process 1 and sends a saturation message to Process 1.
    Process 2 enters the processing stage and sends a resolution message to its neighbors.
    Process 2 finishes with an eccentricity of 3.
    
Active Phase:
    Process 3 receives activation messages from Process 1.
    Process 3 receives saturation messages from Process 1 and Process 5.
    Process 3 sends a saturation message to Process 5.
    
Activation and Saturation Phase:
    Process 4 receives an activation message from Process 1.
    Process 4 sends a saturation message to Process 1.
    Process 4 enters the processing stage, sends a resolution message to its parent (Process 1), and finishes with an eccentricity of 2.
    
Activation and Saturation Phase:
    Process 5 receives an activation message from Process 3.
    Process 5 sends a saturation message to Process 3.
    Process 5 finishes with an eccentricity of 2.
    
Resolution Phase:
    Process 1 receives saturation messages from Process 0, Process 2, and Process 4.
    Process 1 enters the processing stage, sends a resolution message to its neighbors, and finishes with an eccentricity of 2.
    
Resolution Phase:
    Process 0 enters the processing stage, sends a resolution message to its neighbors, and finishes with an eccentricity of 3.
    Resolution Phase:
    Process 3 enters the processing stage, sends a resolution message to its neighbors, and finishes with an eccentricity of 2.
'''