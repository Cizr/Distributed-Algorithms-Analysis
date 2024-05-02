# Overview
This project tackles a common challenge in distributed computing: performing computations within tree networks. The network's tree structure implies that each entity can distinguish whether it functions as a leaf or an internal node.
The specific focus here is on computing node eccentricities, denoted as 𝑟(𝑥). These eccentricities represent the maximum distance between a given node 𝑥 and any other node in the tree. Eccentricity computation finds applications in various fields, notably in graph theory for tasks like identifying central or influential actors in social networks.
# use case 
Social Networks: Eccentricity analysis in social networks, such as Facebook or Twitter, can identify individuals who play central roles in spreading information or influencing the network's dynamics. Nodes with high eccentricity may represent key influencers or connectors who have a broad reach within their social circles, shaping opinions, trends, and the flow of information.
Financial Networks: Within financial systems, eccentricity analysis can reveal critical banks, financial institutions, or markets that have a significant impact on the overall stability and functioning of the economy. Nodes with high eccentricity in financial networks may correspond to central banks, major financial institutions, or key markets that exert disproportionate influence on market dynamics, liquidity, and systemic risk
# Approach
Initially, a basic approach involves each node broadcasting a request, effectively designating itself as the root of the tree. Through a process akin to convergecast on this rooted tree, each node collects the maximum distance to itself. However, this method's scalability is limited, leading to suboptimal complexity.
To address this, a more efficient solution employing the saturation method is proposed. This method leverages saturation to compute the eccentricity of two saturated nodes, subsequently providing the necessary information for other nodes to compute their eccentricities in an optimal manner.

# Algorithm Design

Methodology
Each node within the tree possesses knowledge of its neighbors and its role as a leaf or internal node. Initially, all processing nodes are in an AVAILABLE state.
Nodes transition through several states:

AVAILABLE: The initial state of nodes.
ACTIVE: Nodes awaiting saturation.
PROCESSING: Nodes that have undergone saturation.
SATURATION: Nodes initiating the resolution phase.
DONE: Terminal state indicating completion of execution
![image (2)](https://github.com/Cizr/Distributed-Algorithms-Analysis/assets/100844208/a0fb25e7-0832-474b-b083-2ce2f2a5adc3)
![image (3)](https://github.com/Cizr/Distributed-Algorithms-Analysis/assets/100844208/01a10d76-1f7d-4b08-85f2-f4ee47df6506)

Example 
![White Black Minimalist Classy Notepad (2)](https://github.com/Cizr/Distributed-Algorithms-Analysis/assets/100844208/9f78316a-5ca4-4d0e-96a2-ca0d66247e3c)
Given the above tree, the eccentricities of vertices are:
x(0) = 3 x(1) = 2 x(2) = 3
x(3) = 3 x(4) = 2 x(5) = 3

In summary, the demonstration establishes that precisely two processing nodes will become saturated, and these nodes are neighboring and serve as each other’s parent. This is evidenced by the protocol where an entity only sends a saturation message to its parent and becomes saturated upon receiving a saturation message from its parent.
For instance, when traversing the tree upward from an arbitrary node 'U' a saturated node 'S1' is encountered, implying that its parent'S2' must have been processing and considered S1 as its child The lemma holds true because if there were more than two saturated nodes, there would be a pair of saturated nodes 
x and y such that the distance between them d(x,y) is at least 2, contradicting the saturation condition.

Importantly, the saturation of nodes is unpredictable due to communication delays, and subsequent executions with the same initiators may yield different results. Any pair of neighboring nodes could potentially become saturated. The correctness of the algorithm stems from the fact that at least two saturated nodes possess their eccentricity information and disseminate it to others for computation.
Regarding complexity analysis, the message complexity involves n+k*-2  messages for activation
n messages for saturation, and n−2 messages for resolution, totaling to 
3n+k*−2 messages. Thus, the message complexity is O(n).
the time complexity for finding eccentricities is

T[Eccentricities]=T[FullSaturation]+max{d(s,x):s∈Sat,x∈V}.
