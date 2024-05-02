import graphviz

class Node:
    def __init__(self, id, value):
        '''
        Initializes the Node object.

        Args:
            id (int): The unique identifier of the node.
            value (int): The value associated with the node.
        '''
        self.id = id
        self.neighbors = []
        self.parent = None
        self.status = "ASLEEP"
        self.value = value
        self.depth = 0  # Depth

    def receive_wakeup(self, sender):
        '''
        Receives a wake-up signal from a neighbor node.

        Args:
            sender (Node): The node sending the wake-up signal.
        '''
        #if the node is asleep, wake it up and propagate the wake-up signal to its neighbors
        if self.status == "ASLEEP":
            self.status = "AWAKE"
            for neighbor in self.neighbors:
                if neighbor != sender:
                    neighbor.receive_wakeup(self)

    def send_saturation_message(self, value):
        '''
        Sends saturation messages to neighbor nodes.

        Args:
            value (int): The value to be propagated in the saturation message.
        '''
        if self.status == "AWAKE":
            # Send saturation messages to its neighbors
            for neighbor in self.neighbors:
                neighbor.receive_saturation_message(self, value)

    def receive_saturation_message(self, sender, value):
        '''
        Receives a saturation message from a neighbor node.

        Args:
            sender (Node): The node sending the saturation message.
            value (int): The value received in the saturation message.
        '''
        if self.status == "AWAKE":
            # Update its value based on the received saturation message
            if self.value is None or value < self.value:
                self.value = value
            self.send_saturation_message(value)

    def send_resolution_notification(self, value):
        '''
        Sends resolution notifications to neighbor nodes.

        Args:
            value (int): The minimum value holder to be notified.
        '''
        if self.status == "PROCESSING":
            # Send resolution notifications to its neighbors
            for neighbor in self.neighbors:
                if neighbor != self.parent:
                    neighbor.receive_resolution_notification(value)
            print("Node", self.id, "notified with minimum value holder:", value)

def wakeup(node):
    '''
    Wakes up a node and propagates the wake-up signal to its neighbors.

    Args:
        node (Node): The node to be woken up.
    '''
    # If the node is asleep, wake it up and propagate the wake-up signal to its neighbors
    if node.status == "ASLEEP":
        node.status = "AWAKE"
        for neighbor in node.neighbors:
            neighbor.receive_wakeup(node)

def calculate_depth(node, parent=None, depth=0):
    '''
    Calculates the depth of each node in the tree.

    Args:
        node (Node): The node for which depth is to be calculated.
        parent (Node): The parent node of the current node.
        depth (int): The depth of the current node in the tree.
    '''
    node.depth = depth
    for neighbor in node.neighbors:
        if neighbor != parent:
            calculate_depth(neighbor, node, depth + 1)

tree_structure = {
    0: [1, 2, 3],
    1: [4, 5],
    2: [],
    3: [],
    4: [],
    5: []
}

# Create nodes based on tree structure
nodes = {}
for id, children in tree_structure.items():
    nodes[id] = Node(id, id)

# Connections
for id, children in tree_structure.items():
    parent_node = nodes[id]
    for child_id in children:
        child_node = nodes[child_id]
        # Add the child node to the parent's neighbors and vice versa
        parent_node.neighbors.append(child_node)
        child_node.neighbors.append(parent_node)
        child_node.parent = parent_node

calculate_depth(nodes[0])

node_values = {0: 10, 1: 3, 2: 6, 3: 5, 4: 6, 5: 8}
for node_id, value in node_values.items():
    nodes[node_id].value = value

initiators = [nodes[0]]
network = list(nodes.values())

# To wake up all nodes
for initiator in initiators:
    wakeup(initiator)

# Step 2 Saturation phase
leaf_nodes = [node for node in network if not node.neighbors]  # Find leaf nodes
for leaf in leaf_nodes:
    leaf.send_saturation_message(leaf.value)

# Find minimum value from initiator
minimum_value = min(node_values.values())

# Step 3 Notification phase
for node in network:
    if node.value == minimum_value:
        node.send_resolution_notification(minimum_value)

n = len(network)
k = len(initiators)
messages_min_finding = 3 * n + k - 4

print("Awake nodes:", [(node.id, node.depth) for node in network if node.status == "AWAKE"])
print("Unit of time:", max(node.depth for node in network))
print("Number of messages sent:", n + k - 2)
print("Minimum value found by initiator:", minimum_value)
print("Number of messages for minimum finding (M[MinF-Tree]):", messages_min_finding)
print("All nodes are notified that the minimum value holder is node number", [node.id for node in network if node.value == minimum_value][0])

def draw_tree(network, minimum_value_holder):
    '''
    Draws the tree structure using Graphviz.

    Args:
        network (list): List of Node objects representing the network.
        minimum_value_holder (Node): The node holding the minimum value.
    '''
    dot = graphviz.Digraph(format='png')
    for node in network:
        dot.node(str(node.id), label=f"Node {node.id}\nValue: {node.value}")
        if node.parent:
            dot.edge(str(node.parent.id), str(node.id))
    dot.node(str(minimum_value_holder.id), style="filled", fillcolor="red", label=f"Node {minimum_value_holder.id}\nValue: {minimum_value_holder.value}")
    dot.render('tree', view=True)

# Add parent assignment during node creation
for id, children in tree_structure.items():
    parent_node = nodes[id]
    for child_id in children:
        child_node = nodes[child_id]
        parent_node.neighbors.append(child_node)
        child_node.neighbors.append(parent_node)
        child_node.parent = parent_node

draw_graph = input("Do you want to visualize the tree? (Y/N): ").upper() == "Y"
if draw_graph:
    minimum_value_holder = [node for node in network if node.value == minimum_value][0]
    draw_tree(network, minimum_value_holder)
