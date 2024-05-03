import math

class TreeElection:
    def __init__(self, n, k_star):
        """
        Initializes a TreeElection object.

        Args:
            n (int): Number of nodes in the tree.
            k_star (int): Some constant value.
        """
        self.n = n
        self.k_star = k_star

    def elect_minimum(self):
        """
        Calculates the number of message transmissions for Elect Minimum algorithm.

        Returns:
            int: Number of message transmissions.
        """
        # Calculate the number of message transmissions
        messages = 3 * self.n + self.k_star - 4
        return messages

    def elect_root(self):
        """
        Calculates the number of message transmissions for Elect Root algorithm.

        Returns:
            int: Number of message transmissions.
        """
        # Calculate the number of message transmissions
        messages = 3 * self.n + self.k_star - 2
        return messages

    def elect_minimum_bits(self, id_bits):
        """
        Calculates the number of bits transmitted for Elect Minimum algorithm.

        Args:
            id_bits (int): Number of bits for node identity.

        Returns:
            int: Total number of bits transmitted.
        """
        # Calculate the number of bits transmitted for Elect Minimum
        signals = 2 * self.n + self.k_star - 2
        values = self.n * (id_bits + math.ceil(math.log2(self.n)))
        total_bits = signals + values
        return total_bits

    def elect_root_bits(self, id_bits):
        """
        Calculates the number of bits transmitted for Elect Root algorithm.

        Args:
            id_bits (int): Number of bits for node identity.

        Returns:
            int: Total number of bits transmitted.
        """
        # Calculate the number of bits transmitted for Elect Root
        signals = 3 * self.n + self.k_star - 2
        values = 2 * (id_bits + math.ceil(math.log2(self.n)))
        total_bits = signals + values
        return total_bits

#usage
n = 10  #Num of nodes in the tree
k_star = 5  #Some constant value
id_bits = 16  #Num of bits for node identity

election = TreeElection(n, k_star)

#Calculate the number of message transmissions
min_messages = election.elect_minimum()
root_messages = election.elect_root()

print("Elect Minimum Messages:", min_messages)
print("Elect Root Messages:", root_messages)

#Calculate the number of bits transmitted
min_bits = election.elect_minimum_bits(id_bits)
root_bits = election.elect_root_bits(id_bits)

print("Elect Minimum Bits:", min_bits)
print("Elect Root Bits:", root_bits)


#OUTPUT
'''
PS C:\Users\dadyk\Desktop\DISTRIBUTED ALGORITHMS> 
Elect Root Messages: 33
Elect Minimum Bits: 223
Elect Root Bits: 73.
PS C:\Users\dadyk\Desktop\DISTRIBUTED ALGORITHMS> 

'''
