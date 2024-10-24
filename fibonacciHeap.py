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
        key_set(set): stores unique keys to avoid duplication
    """
    def __init__(self):
        # Initialize the Fibonacci heap with no minimum node, an empty root list, and zero node count
        self.mMinimum = None   
        self.rootlist = Fibtree() # The root list is managed as a forest of Fibonacci trees
        self.node_count = 0
        self.key_set = set()  # A set to store unique keys


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


    def isEmpty(self):
        """
        Check if the Fibonacci heap is empty.

        Returns:
            bool: True if the heap is empty, False otherwise.
    
        Prints:
            A message indicating whether the heap is empty or not.
        """
        
        empty = self.mMinimum is None
        if empty:
            print("the heap is empty")
        else:
            print("The heap is not empty")
        return empty


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
        """
        Merges two Fibonacci heaps and returns the resulting heap.

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
        """
        Print the keys and priorities of the nodes in the root list of the Fibonacci heap.

        This function traverses the root list and prints the priority and key of each node.
        It uses a set to keep track of visited nodes to avoid infinite loops in case of circular references.

        Returns:
            None
        """
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
        

   
    def consolidate(self):
        """
        Consolidates the trees in the root list of the Fibonacci heap by merging
        trees of equal degree together. 

        The function iterates through the root list and uses a dictionary to
        keep track of trees by their degree. If two trees have the same degree,
        the tree with the higher priority becomes a child of the tree with the 
        lower priority using the helper function `fib_Link`. This process continues
        until all trees in the root list have distinct degrees.

        Updates:
            - The minimum node (mMinimum) in the heap.
            - The root list of the heap.
    
        Raises:
            None.
        """
        # Dictionary to store nodes by their degree 
        nodes = defaultdict(list)

        # initialize variable current as the minimum node
        current = self.rootlist.head 

        # Handle the case where the heap is empty
        if current is None:
            return
        
        # Handle the case where there is only one element in the heap
        if current.prev == current.next == current:
             self.mMinimum = current
             self.rootlist.head = None 
             return  

        # since the list is circular, this avoids visiting a node more than once
        visited_nodes = set()
        
        while current and current not in visited_nodes: 
            visited_nodes.add(current)
            
            x = current
            degree = current.degree
            current = current.next

            # Merge trees of the same degree
            while degree in nodes and nodes[degree] is not None:
                y = nodes[degree]

                #if x has a higher priority, swap places
                if x.priority > y.priority:
                    y, x = x, y    
                          
                self.fib_Link(y, x)
                nodes[degree] = None
                
                degree += 1
                
            nodes[degree] = x
            
        # Reset the minimum node and rebuild the root list    
        self.mMinimum = None
        self.rootlist.head = None
        for trees in nodes.values():
            if trees:
                self.rootlist.add_to_root_list(trees)
                if self.mMinimum is None or trees.priority < self.mMinimum.priority:
                    self.mMinimum = trees
            
        
    def extractMin(self):
        """
        Extracts the node with the minimum priority from the Fibonacci heap.
        
        This method removes the minimum node from the heap, adds its children to the root list,
        and consolidates the heap to maintain its properties.

        Raises:
            ValueError: If the heap is empty.

        Returns:
            Node: The extracted minimum node.
        """
        # check if heap is empty as you cannot extract 
        #from an empty heap
        if self.isEmpty():
            raise ValueError("Empty Heap")

        # ensure the element to be remove is the minimum
        minElem = self.mMinimum
      
        if minElem is not None:
            child = minElem.children.head
            while child is not None:           
                minElem.children.add_to_root_list(child)
                child.parent = None
                child = child.next
                
                #break circular link
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
    
    

    def fib_decrease(self, x, priority):
        """
        Decreases the key (priority) of the given node x in the Fibonacci heap.
            
        This function ensures that the new key is less than the current key.
        If the new key violates the min-heap property, an exception is raised.
    
        If the node x is a root and its parent has a key greater than x's,
        x is cut from its parent to maintain the min-heap order. If x's new key
        is less than the current minimum, it updates the minimum node of the heap.

        Args:
            x: The node whose key is to be decreased.
            priority: The new priority to be assigned to node x.

        Raises:
            ValueError: If the new priority is greater than the current priority of x.
        """
        
        # Check that the min-heap order property is not violated
        if priority > x.priority:
            print(f"new {priority} is greater than {x.priority}")
            return
            
        # Update the priority of the node if new priority is smaller
        x.priority = priority
        
        y = x.parent  

        # Check if the node has a parent and if the min-heap order is violated
        if y is not None and x.priority < y.priority:
            self.cut(x,y)  #Cut x from its parent
            self.cascadingCut(y) #Perform cascading cut on the parent y

         # Update the minimum node if necessary
        if x.priority < self.mMinimum.priority:
            #save x as the new heap minimum
            self.mMinimum =  x
            

    def cut(self, x, y):
        """
        Cuts node x from its parent node y in the Fibonacci heap.

        This function removes node x from the child list of y, decrements the degree 
        of y, and adds node x to the root list of the heap. This operation is performed
        when the priority of node x is decreased and violates the min-heap property.

        Args:
            x: The node to be cut from its parent.
            y: The parent node from which x is to be removed.

        Raises:
            ValueError: If x does not have a parent.
        """
        
        # x can only be cut if it is link to another node as child
        if x.parent is None:
            raise ValueError("x does not have a parent")
            
        #remove x from the childlist of y
        y.remove_from_childlist(x)
        
        # Decrement the degree of y since x is no longer a child
        y.degree -= 1
        
        # Add x to the root list
        self.rootlist.add_to_root_list(x)
        
        # Update the parent of x to None and reset the mark
        x.parent = None
        x.mark = False

    def cascadingCut(self, y):
        """
        Performs a cascading cut operation on node y in the Fibonacci heap.

        This function marks node y if it is not already marked. If y is marked, 
        it cuts y from its parent z and recursively applies cascading cut on z.
    
        Args:
            y: The node to perform cascading cut on. 
        """
        # initialize a variable z as y parent
        z = y.parent
        if z is not None:
            # If y is not marked, mark it. A node can be mark if it has lost a child
            if y.mark == False:
                y.mark = True
            else:
                # Cut y from its parent z
                self.cut(y, z)
                # Recursively apply cascading cut on parent z
                self.cascadingCut(z)

    def delete(self, x):
        """
        Deletes node x from the Fibonacci heap.

        This function first decreases the key of node x to positive infinity,
        effectively making it the minimum node, and then extracts the minimum node,
        which removes x from the heap.

        Args:
            x: The node to be deleted from the Fibonacci heap.
    
        Raises:
            ValueError: If x is None or not found in the heap.
        """
        # Decrease the key of node x to positive infinity
        self.fib_decrease(x, math.inf("inf") )
        
         # Extract the minimum node, which will remove x from the heap
        self.extractMin()
        
        
