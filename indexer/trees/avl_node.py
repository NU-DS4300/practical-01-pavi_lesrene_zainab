from typing import List, Optional, Any
from indexer.trees.bst_node import BSTNode

class AVLNode(BSTNode):
    """
    AVLNode class represents a node in an AVL tree. It inherits from BSTNode
    adds 1 additional attribute, height, used in balancing the tree.

    Attributes:
        key (Any): The key value stored in the node.
        height (int): The height of the node in the AVL tree.

    Methods:
        __init__(key: Any): Initializes a new instance of the AVLNode class 
        with the given key.
    """
    def __init__(self, key: Any):
        super().__init__(key)
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1
