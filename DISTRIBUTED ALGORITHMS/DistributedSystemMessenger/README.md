# Chat System with Broadcasting

## Overview
This project entails the development of a chat system comprising a server and multiple clients, each serving as nodes within the network. The server includes a Supervisor thread, while each client contains both a Controller thread and an Application thread.

## Components
### Supervisor Thread
- Oversees the execution of the application.
- Receives copies of exchanged messages and information regarding entity states.
- Displays real-time metrics such as the number of messages exchanged and elapsed time.

### Controller Threads
- Implement the distributed algorithm.
- Communicate with the Supervisor thread by transmitting message copies (via Send and Receive operations) and state information.
- Implement the Send and Receive operations.

### Application Threads
- Display activities occurring at the Controller thread level.

## Application Network
- Represented within the Controller threads by a table, mirroring the chosen algorithm's network structure (tree, ring, complete graph).
  
Overview for main idea: 
![planning](https://github.com/Cizr/Distributed-Algorithms-Analysis/assets/100844208/bb6fe85a-7b4b-4625-b369-c4b497559e4e)

The system is designed to facilitate seamless communication among multiple clients, each equipped with dedicated threads for handling message exchange and application-level interactions.

One of the standout features of our implementation is its peer-to-peer communication model, which empowers clients to interact directly with one another without heavy reliance on the server. Moreover, we've integrated robust broadcasting functionality, allowing clients to effortlessly disseminate messages to all connected peers by leveraging a straightforward "/broadcast" command.

To ensure comprehensive testing and evaluation, we've meticulously crafted three distinct network topologies: Tree, Ring, and Fully Connected. These topologies serve as invaluable tools for assessing the system's performance and resilience under varying network conditions, thereby bolstering its overall reliability and scalability.
![Sans_titre](https://github.com/Cizr/Distributed-Algorithms-Analysis/assets/100844208/0017e5ec-efd3-42ce-a7fe-793a1ff1ec75)

we employed a  trick to calculate the unit of time for message propagation within the network topology. 
Leveraging the concept of depth between nodes, we established a simple yet effective metric wherein each unit of depth between nodes corresponded to one unit of time. This approach enabled us to intuitively quantify the time required for messages to traverse from one node to another based on their relative positions within the network structure. 
