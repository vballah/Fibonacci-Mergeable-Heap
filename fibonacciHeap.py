import math
from collections import defaultdict
from math import inf as infinity
from nodes import Node
from fibtree import Fibtree


class FibHeap:
    """
     A class representing a Fibonacci heap data structure.

    This implementation supports efficient priority queue operations, including insertion,
    extraction of the minimum element, and merging of heaps. It utilizes a collection of 
    trees and maintains the Fibonacci heap properties.

    Attributes:
        mMinimum (Node): The minimum node in the Fibonacci heap.
        rootlist (Fibtree): The root list containing trees of the heap.
        node_count (int): The total number of nodes in the heap.
    """
    def __init__(self):
        # Initialize the Fibonacci heap with no minimum node, an empty root list, and zero node count
        self.mMinimum = None   
        self.rootlist = Fibtree() # The root list is managed as a forest of Fibonacci trees
        self.node_count = 0


    def insert(self, key, priority):
        """
            Inserts a new node into the Fibonacci heap.

            This method adds a node with the specified key and priority. If the heap is empty,
            it creates a singleton tree. Otherwise, it compares the new node's priority with the
            current minimum and updates the minimum if necessary.

            Args:
                key: The key associated with the node to be inserted.
                priority (float): The priority of the node.

            Raises:
                ValueError: If the provided priority is None or invalid.

            Returns:
                 Node: The newly created node.
        """
        priority = self.checkPriority(priority) 
        new_node =  Node(key,priority)
        
        if self.mMinimum is None:
            self.rootlist.add_to_root_list(new_node)   
            self.mMinimum = new_node   
            
        else: 
            self.rootlist.add_to_root_list(new_node)  
            if new_node.priority < self.mMinimum.priority:
                self.mMinimum = new_node  

        self.node_count += 1
        print(f"Inserted {key} with priority {priority}. Total nodes: {self.node_count}")
        return new_node
         
    #check priority
    def checkPriority(self, priority):
        if priority is None:
            raise ValueError("priority cannot be None")
        
        try:
            priority = float(priority)
        except ValueError:
            raise ValueError(f"invalid priority value: {priority}")
        
        if math.isnan(priority):
            raise ValueError(f"{priority} is invalid: cannot be NaN.")
        return priority

    #check if the heap is empty in 0(1).
    def isEmpty(self):
        empty = self.mMinimum is None
        if empty:
            print("the heap is empty")
        else:
            print("The heap is not empty")
        return empty


    #the below function finds the minimum node in the heap in 0(1) time
    def getMin(self):
         """
         Retrieves the minimum node from the Fibonacci heap.
            This operation checks whether the heap is empty and returns the node with the minimum
            priority.

        Returns:  
            Node: The node with the minimum priority, or None if the heap is empty.
        """
        if self.isEmpty():
            return None
        return self.mMinimum
    
   
    def fib_Union(self, other):
        """Merges two Fibonacci heaps and returns the resulting heap.

        Args:
            other (FibHeap): The other Fibonacci heap to merge with this one.

        Returns:
            FibHeap: The merged Fibonacci heap.
        """
        if self.mMinimum is None:
            return other
        
        if other.mMinimum is None:
           return self
    

        #link the two list in a circular fashion
        self.rootlist.last.next = other.rootlist.head
        other.rootlist.head.prev = self.rootlist.last
        self.rootlist.last = other.rootlist.last
        
        if( other.mMinimum.priority < self.mMinimum.priority):
            self.mMinimum = other.mMinimum

        # increment the count of the nodes in the merge heap
        self.node_count += other.node_count
        
        other.rootlist.head = None
        other.mMinimum = None
        other.node_count = 0
        
        #return self, the new mergeable heap
        return self
    
    def print_union(self):
        visited = set()
        current = self.rootlist.head
        while current and current not in visited:
            visited.add(current)
            print(f"priority: {current.priority}, key: {current.key}")
            current = current.next
            if current == self.rootlist.head:
                break
        visited.add(current)
        
     
    def fib_Link(self, y, x):
        """
        Links two nodes in a Fibonacci heap by making node y a child of node x.

        This function checks that both nodes are valid and that node y does not 
        already have a parent. It ensures that node x has a priority less than 
        or equal to node y's priority before linking. If the conditions are met, 
        node y is removed from the root list and added to the child list of node x, 
        and the degree of node x is updated accordingly.

        Args:
            y (Node): The node to be linked as a child.
            x (Node): The node to be linked to (parent).

        Raises:
            ValueError: If either x or y is None.
            ValueError: If node y already has a parent.
            ValueError: If node y is not in the root list.
            ValueError: If x's priority is greater than y's priority.

        """
        # Check if both x and y are present in the rootlist
        if x is None or y is None:
            raise ValueError("Neither x nor y can be None.")

    # Check if y already has a parent
        if y.parent is not None:
            raise ValueError("Node y already has a parent.")
            
        # add y in x child list
        x.children.add_to_root_list(y)
        
    # Check if y is in the root list
        if self.rootlist.head is None or (y.prev is None and y.next is None):
            raise ValueError("Node y is not in the root list.")

    # Check if x's priority is less than or equal to y's priority
        if x.priority <= y.priority:
    
         
        # Remove y from the root list
            self.rootlist.remove_from_root_list(y)
        
        # Add y to the child list of x
            x.add_to_child_list(y)
            y.parent = x
        
        # Update the degree of x
            x.degree += 1
        
        # Reset the mark of y
            y.mark = False
        
        # Print the successful linking
            print(f"Added child {y.key} to parent {x.key}. New degree: {x.degree}")
        else:
           raise ValueError("Cannot link y as a child of x because y's priority is lower than x's priority.")
        

    # the consolidate function reduces the number of trees in the rootlist by merging
    # trees of equal degree together. given two trees x and y in the rootlist with the same degree, 
    # if x.key <= y.key, the helper function Fib_Link will make y a child of x, thus merging Y with x.
    # this happens until only trees of distinct degree are in the rootlist.
    def consolidate(self):
        #need to find a way to store elements from the rootlist 
        #in the dictionary with their degrees   
        nodes = defaultdict(list)
        current = self.rootlist.head 
        
        if current is None:
            return
        
        #only one element in the heap
        if current.prev == current.next == current:
             self.mMinimum = current
             self.rootlist.head = None 
             return  
         
        visited_nodes = set()
        
        while current and current not in visited_nodes: 
            visited_nodes.add(current)
            
            x = current
            degree = current.degree
            current = current.next
            
            while degree in nodes and nodes[degree] is not None:
                y = nodes[degree]
                
                if x.priority > y.priority:
                    y, x = x, y    
                          
                self.fib_Link(y, x)
                nodes[degree] = None
                
                degree += 1
                
            nodes[degree] = x
            
        self.mMinimum = None
        self.rootlist.head = None
        for trees in nodes.values():
            if trees:
                self.rootlist.add_to_root_list(trees)
                if self.mMinimum is None or trees.priority < self.mMinimum.priority:
                    self.mMinimum = trees
            
        
                    
            
   


    #the following procedure extracts the minimum node 
    # from the rootlist in the heap and adds it children
    # to the rootlist, if it has
    # this works by first making a root out of the minimum node children
    # and then extracting the minimum node from the rootlist while maintaining the heap property
    #the helper function consolidates ensure that each root elements merging in the rootlist
    #  have distinct degree
    def extractMin(self):
        if self.isEmpty():
            raise ValueError("Empty Heap")
        
        minElem = self.mMinimum
      
        if minElem is not None:
            child = minElem.children.head
            while child is not None:           
                minElem.children.add_to_root_list(child)
                child.parent = None
                child = child.next
                if child == minElem.children.head:
                    break
                    
            self.rootlist.remove_from_root_list(minElem)
            
            if minElem == minElem.next:
                self.mMinimum = None 
            else:
                self.mMinimum = minElem.next
                
                self.consolidate() 
            self.node_count -= 1
        
        return minElem
    
    
            
    
    #the following function decrease key ensures that the new  key to be
    #inserted is less than the current key, otherwise an exception is thrown.
    # if the node who key is to be decrease is a root and it has parent with key
    # greater than the node, then min-heap order is violated and that node is cut from 
    # it's parent, else the node and key is save as the new minimum
    def fib_decrease(self, x, priority):
        if priority > x.priority:
            print(f"new {priority} is greater than {x.priority}")
            return
        x.priority = priority
        y = x.parent    
        if y is not None and x.priority < y.priority:
            self.cut(x,y)
            self.cascadingCut(y)
        if x.priority < self.mMinimum.priority:
            #save x as the new heap minimum
            self.mMinimum =  x

    # this function removes node from the  childlist of y
    # decrementing y degree and adding node to the rootlist.
    # this is a helper function for decrease key as in the case where y is a 
    # parent of node but y key is greater than node, which violates min-heap
    def cut(self, x, y):
        if x.parent is None:
            raise ValueError("x does not have a parent")
        #remove x from the childlist of y
        y.remove_from_childlist(x)
        y.degree -= 1
        self.rootlist.add_to_root_list(x)
        x.parent = None
        x.mark = False

    def cascadingCut(self, y):
        z = y.parent
        if z is not None:
            if y.mark == False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascadingCut(z)

    def delete(self, x):
        self.fib_decrease(x, math.inf("inf") )
        self.extractMin()
        
        
