class Fibtree: 
    """ 
        Represents the root list of min-ordered mergeable trees used in a Fibonacci heap.

        The root list is implemented as a circular doubly linked list, which facilitates 
        fast lookup, insertion, and other operations. 

        A node can be added to the root list if it is not a child of any other nodes 
        or if it has a smaller priority than its parent. 

        Nodes can be removed from the root list during the Extract-Min operation or 
        the linking operation.

        Attributes:
            head: The first node in the circular linked list (the minimum node).
            last: The last node in the circular linked list.
    
        Methods:
            add_to_root_list(node): 
                Adds a new node to the root list.
                Returns:
                 None
            
            remove_from_root_list(node): 
                Removes a specified node from the root list.
                Returns:
                    None
            
            traverse(): 
                Traverses the root list and prints each node's key and priority.
                Returns:
                    None
        """  
    def __init__(self):
        # Initialize the head and last pointers of the root list to None.
        self.head = None
        self.last = None
        
        
    def add_to_root_list(self, node):
        """
        Add a node to the root list of the Fibonacci heap.

        This function maintains the circular doubly linked structure of the root list.
        If the root list is empty, it initializes the head and last pointers to the new node.
        If the root list is not empty, it adds the new node to the end of the list and updates the pointers accordingly.

        Args:
            node: The node to be added to the root list.

        Returns:
            None
        """
         # If the root list is empty, initialize head and last to the new node.
        if not self.head:
            self.head = node
            self.last = node          
            node.next = node.prev = node # Point next and prev to itself (circular)
            
         # Add the node to the root list, updating pointers to maintain circular structure.
        else:
            node.next = self.head
            node.prev  = self.last
            self.last.next = node
            self.head.prev = node
            self.last = node
    
    
    def remove_from_root_list(self, node):
        """
        Remove a node from the root list of the Fibonacci heap.

        This function handles the removal of a node, adjusting the circular doubly linked 
        structure of the root list accordingly. If the node to be removed is the only element,
        both head and last pointers are set to None. If the node is the head, the head pointer
        is updated to the next node.

        Args:
            node: The node to be removed from the root list.

        Raises:
            ValueError: If the list is empty or if the node does not exist in the list.

        Returns:
            None
        """
        # Raise an error if trying to remove from an empty list.
        if not self.head:
            raise ValueError("cant remove from empty list")
        
        print(f"removing node: {node.key}")
        if node is None:
           raise ValueError("node doen't exist") 
       
        # If the node to remove is the head of the list (the minimum node).
        if node == self.head:
            if self.head == self.last:
               print("node is the only element in list")
               self.head =  self.last = None    
                  
            else:
                # Update head to the next node and adjust links.
                self.head = node.next
                node.prev.next = node.next
                node.next.prev = node.prev
              
        else: 
            node.prev.next = node.next
            node.next.prev = node.prev
            
        # Clear the pointers of the removed node.       
        node.prev = node.next = None
        node.parent = None
   
            
    def traverse(self):
        visited = set()

        if not self.head:
            print("empty tree")
            return
        
        node = self.head
        print("traversing the tree:")
        
        while node and node not in visited:
            visited.add(node)
            print(f"node key: {node.key}, priority: {node.priority}")
            
            node = node.next
            
            if node == self.head:
                break
    
        visited.add(node)
       
