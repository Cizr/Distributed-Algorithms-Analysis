# Summary:
The Minimum Finding (MinFind) problem involves determining the smallest value distributed among the nodes of a network. Each node initially holds an input value, and the goal is for every node to ascertain whether its value is the minimum. This problem is crucial in distributed query processing, where data is distributed across network sites, and queries can arrive at any time, triggering computation and communication activities.

In a tree network, if rooted, the Minimum Finding problem can be solved by performing a broadcast down from the root to compute the minimum value, followed by a convergecast to determine the minimum value at the root. However, in unrooted trees, Full Saturation can achieve the same goal without a root or additional information. Full Saturation entails nodes sending the smallest known value in the saturation stage, and the two saturated nodes later notify the network of the minimum value they have computed.
# Algorithm

![image (4)](https://github.com/Cizr/Distributed-Algorithms-Analysis/assets/100844208/15d0fb94-2daa-4496-8940-a50adc86995f)

Cost : 
M[MinF − Tree] = 3n + k' − 4
![image (5)](https://github.com/Cizr/Distributed-Algorithms-Analysis/assets/100844208/9df403b8-3ef1-4729-ad7c-7c2d45635dea)
