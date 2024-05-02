# Summary:
The Minimum Finding (MinFind) problem involves determining the smallest value distributed among the nodes of a network. Each node initially holds an input value, and the goal is for every node to ascertain whether its value is the minimum. This problem is crucial in distributed query processing, where data is distributed across network sites, and queries can arrive at any time, triggering computation and communication activities.

In a tree network, if rooted, the Minimum Finding problem can be solved by performing a broadcast down from the root to compute the minimum value, followed by a convergecast to determine the minimum value at the root. However, in unrooted trees, Full Saturation can achieve the same goal without a root or additional information. Full Saturation entails nodes sending the smallest known value in the saturation stage, and the two saturated nodes later notify the network of the minimum value they have computed.
# Algorithm

![image (4)](https://github.com/Cizr/Distributed-Algorithms-Analysis/assets/100844208/15d0fb94-2daa-4496-8940-a50adc86995f)
# Cost : 
M[MinF − Tree] = 3n + k' − 4
-Awake nodes: [(0, 0), (1, 1), (2, 1), (3, 1), (4, 2), (5, 2)]
-Unit of time: 2
-Number of messages sent: 5
-Minimum value found by initiator: 3
-Number of messages for minimum finding (M[MinF-Tree]): 15
-All nodes are notified that the minimum value holder is node number 1
