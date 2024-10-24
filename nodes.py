from fibtree import Fibtree

class Node:
    """
        Initialize a new node for the Fibonacci heap.

        Args:
            key: The unique identifier for the node.
            priority: The priority value of the node, used for ordering in the heap.

        Attributes:
            parent: The parent node of this node in the heap. Defaults to None.
            prev: The previous node in the circular doubly linked list. Defaults to None.
            next: The next node in the circular doubly linked list. Defaults to None.
            mark: A boolean indicating if the node has lost a child. Defaults to False.
            degree: The number of children this node has. Defaults to 0.
            children: A Fibonacci tree instance representing the children of this node.
    """
    def __init__(self,key, priority):  
        self.key = key 
        self.priority = priority 
        self.parent = None
        self.prev = None
        self.next = None
        self.mark = False
        self.degree = 0
        self.children = Fibtree()  # Initialize children as a Fibonacci tree
        
    def add_to_child_list(self, child):
        
        if child is None:
            raise ValueError("child cannot be none")
         
        if child.parent is not None:         
            print(f"Child {child.key} already has a parent {child.parent.key}. Removing from current parent.")
            child.parent.remove_from_child_list(child)
        
        current = self.children.head
        
        while current is not None:
            if current.priority == child.priority: 
                print(f"Child {child.key} is already a child of {self.key}")
                return
                
            current = current.next
            if current == self.children.head:
                break   
            
            
        self.children.add_to_root_list(child) 
        child.parent = self
        self.degree += 1
        print(f"Added child {child.key} to parent {self.key}. New degree: {self.degree}")
        
        
    def remove_from_child_list(self,child ):
        if child is None:
            raise ValueError("child cannot be none")
        
        # Assuming children is a circular doubly linked list
        if self.children.head is None:
           print(f"No children to remove from {self.key}.")
           return
    
        if child and child.parent == self:          
            self.children.remove_from_root_list(child)
            child.parent = None
            self.degree -= 1
                        
  

    def __str__(self) -> str:
        return f"Key: {self.key}, Priority: {self.priority}"
