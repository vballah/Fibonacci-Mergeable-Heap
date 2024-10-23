# Fibonacci Mergeable Heap
The Fibonacci Mergeable Heap is a min-ordered heap that implements a priority queue, where the keys are characters and the values are numbers. This data structure consists of a collection of trees (a forest), where each node can have children (with defined degrees and edges) or exist as a singleton tree within the heap.

## Description
The project implements a Fibonacci Mergeable Heap, which maintains a min-ordered structure.

## Key Operations of the project includes:

- Insert: Nodes can only be added to the root list if they have the smallest priority compared to all other nodes in the heap.
- FindMinimum: Retrieves the node with the minimum priority without removing it from the heap.
- ExtractMinimum: This operation retrieves and removes the node with the minimum priority. It utilizes an array and a Circular Doubly Linked List (CDLL) to manage the degree of each node, enforcing the min-heap order, which is vital for the integrity of the data structure.
- Union (Merge): Combines two Fibonacci heaps into one, maintaining the min-ordered structure.
- DecreaseKey: Allows for updating the priority of a specific node efficiently.
- DeleteKey: Removes a specified node from the heap, adjusting the structure as needed.
Each tree in the forest contains at least one minimum node that is part of the root list. The root list (heap) is managed using a Circular Doubly Linked List, enabling efficient insertions and deletions.

## Why the Project is Useful
This project is particularly useful in pathfinding algorithms, such as A* and Dijkstra's, where the mergeable heap and the extract-min operation help determine the cheapest cost of a path (edges and nodes) from a source node to a destination node.

For example, to travel from source A to destination H, the algorithm evaluates the cost of the cheapest intermediate nodes and selects the best option. By using a Fibonacci Mergeable Heap, these algorithms can run more efficiently, especially in scenarios involving dynamic graphs where frequent updates to paths occur.

## Function Overview
- Insert(H, x): This function inserts node x into the heap. If x has the smallest priority compared to all other nodes in the heap, it becomes the new minimum node.
- FindMinimum(H): Retrieves the node with the minimum priority without removing it from the heap.
- ExtractMinimum(H): Removes and returns the node with the smallest key from the heap. This operation uses an array and a CDLL to manage the degree of nodes, maintaining the min-heap order.
- Union(H1, H2): Combines two heaps, H1 and H2, into a single heap.
- DecreaseKey(H, x, newPriority): Decreases the priority of node x to a new priority value.
- DeleteKey(H, x): Removes the specified node x from the heap, adjusting the structure accordingly.

## Time Complexities
### Operation	Amortized Time Complexity
Insert	O(1)
FindMinimum	O(1)
ExtractMinimum	O(log n)
Union	O(1)
DecreaseKey	O(1)
DeleteKey	O(log n)



