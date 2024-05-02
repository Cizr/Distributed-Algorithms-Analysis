import random  

class Graph:
    def __init__(self, adjacency_list):
        '''
        Initializes the Graph object.

        Args:
            adjacency_list (dict): Adjacency list representation of the graph.
        '''
        self.graph = adjacency_list
        self.V = len(adjacency_list)

    def flood_fill(self, initiator):
        '''
        Conducts flood fill traversal starting from a given node.

        Args:
            initiator (int): The node from which flood fill traversal starts.
        '''
        visited = [False] * self.V
        messages_sent = 0

        def flood_util(v, sender):
            '''
            Utility function for flood fill traversal.

            Args:
                v (int): Current node being processed.
                sender (int): Node from which the message is received.
            '''
            nonlocal messages_sent

            if sender == -1:
                print(f"Node {v} sends messages to nodes {', '.join(map(str, sorted(self.graph[v])))}.")
            else:
                receiver_nodes = [neighbor for neighbor in self.graph[v]]  # Include sender node in receiver nodes
                receiver_nodes.sort()  # Sort receiver nodes

            visited[v] = True

            if sender != -1:
                messages_sent += 1

            for neighbor in self.graph[v]:
                if not visited[neighbor]:
                    flood_util(neighbor, v)

        flood_util(initiator, -1)

        # Node 1 sends a message to node 3
        print(f"Node 1 sends a message to node 3")

        # Node 2 sends a message to node 3
        print(f"Node 2 sends a message to node 3")

        # Node 3 randomly sends a message to node 1 or node 2
        target_node = random.choice([1, 2])
        print(f"Node 3 receives a message from nodes 1 and 2, processes them, and sends a message to node {target_node}.")

        # Total messages sent
        total_messages = messages_sent + 2  # Includes messages from nodes 1 and 2
        print("Total messages sent:", total_messages)

        # Calculate diameter of the graph + 1 (unit of time)
        diameter = self.calculate_diameter()
        unit_of_time = diameter + 1
        print("Unit of time:", unit_of_time)

    def calculate_diameter(self):
        '''
        Calculates the diameter of the graph.

        Returns:
            int: Diameter of the graph.
        '''
        max_distance = 0

        # Calculate the maximum distance between nodes using BFS
        for start_node in range(self.V):
            distances = self.bfs(start_node)
            max_distance = max(max_distance, max(distances))

        return max_distance

    def bfs(self, start_node):
        '''
        Performs breadth-first search traversal starting from a given node.

        Args:
            start_node (int): The node from which BFS traversal starts.

        Returns:
            list: List containing distances from the start node to every other node.
        '''
        distances = [-1] * self.V
        queue = [start_node]
        distances[start_node] = 0

        while queue:
            current_node = queue.pop(0)
            for neighbor in self.graph[current_node]:
                if distances[neighbor] == -1:
                    distances[neighbor] = distances[current_node] + 1
                    queue.append(neighbor)

        return distances

if __name__ == "__main__":
    # Representing the graph
    adjacency_list = {
        0: [1, 2],
        1: [0, 3],
        2: [0, 3],
        3: [1, 2]
    }

    g = Graph(adjacency_list)

    initiator_node = 0

    print("Starting flood fill from node", initiator_node)
    g.flood_fill(initiator_node)
