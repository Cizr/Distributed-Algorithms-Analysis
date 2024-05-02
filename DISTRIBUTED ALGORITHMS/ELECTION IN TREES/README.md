## Tree Election Algorithm
The TreeElection class implements algorithms for electing leaders in a tree network topology. This class provides methods to calculate the number of message transmissions and the total number of bits transmitted for two specific election strategies: Elect Minimum and Elect Root.

# Explanation
The TreeElection class offers methods to analyze two election strategies: Elect Minimum and Elect Root. These strategies are tailored for tree network topologies, where the number of edges (m) equals n-1, representing a sparse configuration.

# Elect Minimum
Elect Minimum optimally seeks the smallest value in the tree using the saturation technique, derived from the MinF-Tree protocol. It aims to minimize message transmissions, with its complexity defined as:
M[Tree:ElectMin]=3n+k∗−4
# Elect Root
Elect Root transforms the network into a rooted tree, simplifying the election process. It leverages Full Saturation and introduces new rules for effective tree rooting. The number of message transmissions for Elect Root is:
M[Tree:ElectRoot]=3n+k∗−2
# Tree Network Topology
The tree network topology represents a connected graph with m = n - 1 edges, where n is the number of nodes. This topology is crucial for understanding the efficiency of the election algorithms.
# Granularity of Analysis: Bit Complexity
Analyzing the strategies at a finer level involves considering the number of bits transmitted, offering deeper insights into efficiency.
Elect Minimum Bits: Involves n value messages during saturation, with a total bits transmitted of:
B[Tree:ElectMin]=n(c+logid)+c(2n+k∗−2)
Elect Root Bits: With only two value messages, Elect Root demonstrates higher bit efficiency, calculated as:
B[Tree:ElectRoot]=2(c+logid)+c(3n+k)
Elect Root outperforms Elect Minimum in terms of bits transmitted, providing a more detailed analysis of algorithm performance.


# verify the calculations:
For Elect Minimum:
Number of messages: 31
The number of bits: 
𝑛(𝑐+log⁡𝑖𝑑)+𝑐(2𝑛+𝑘∗−2)n(c+logid)+c(2n+k∗−2)=31
(𝑐+log⁡𝑖𝑑)+𝑐(2×8+7−2)=31(𝑐+3)+𝑐(15)=31(𝑐+3)+15𝑐=31×4+15×1=124+15=139=31(c+logid)+c(2×8+7−2)=31(c+3)+c(15)=31(c+3)+15c=31×4+15×1=124+15=139

For Elect Root:
Number of messages: 33
Number of bits: 2(𝑐+log⁡𝑖𝑑)+𝑐(3𝑛+𝑘∗−2)2(c+logid)+c(3n+k∗−2)=2
(𝑐+log⁡𝑖𝑑)+𝑐(3×8+7−2)=2(𝑐+3)+𝑐(29)=2(𝑐+3)+29𝑐=2×4+29×1=8+29=37=2(c+logid)+c(3×8+7−2)=2(c+3)+c(29)=2(c+3)+29c=2×4+29×1=8+29=37

Let's compare these calculations to the output:
Elect Minimum Bits: 139
Elect Root Bits: 73
