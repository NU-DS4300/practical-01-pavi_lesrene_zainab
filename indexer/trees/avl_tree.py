import string
from typing import List, Optional, Any

from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.trees.avl_node import AVLNode

class AVLTreeIndex(BinarySearchTreeIndex):
    """
    An AVL Tree implementation of an index that maps a key to a list of values.
    AVLTreeIndex inherits from BinarySearchTreeIndex meaning it automatically
    contains all the data and functionality of BinarySearchTree.  Any
    functions below that have the same name and param list as one in 
    BinarySearchTreeIndex overrides (replaces) the BSTIndex functionality. 

    Methods:
        insert(key: Any, value: Any) -> None:
            Inserts a new node with key and value into the AVL Tree
    """
    
    def __init(self):
       super().__init__()
       self.root: Optional[AVLNode] = None

    
    def _height(self, node: Optional[AVLNode]) -> int:
        """
        Calculate the height of the given AVLNode.

        Parameters:
        - node: The AVLNode for which to calculate the height.

        Returns:
        - int: The height of the AVLNode. If the node is None, returns 0.
        """
        if not node:
            return 0
        return node.height
    

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """
        Performs a right rotation on the AVL tree. For when too many nodes are inserted left.

        Args:
            y (AVLNode): The node to be rotated.

        Returns:
            AVLNode: The new root of the rotated subtree.
        """
        
        #current = new node just added
        current = y.left #y > current
        t2 = current.right #T2 > current and T2 < y

        #rotation: now current will be the root of the tree
        current.right = y 
        y.left = t2 

        #update heights
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        current.height =  1 + max(self._height(current.left), self._height(current.right))

        return current


    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """
        Rotate the given node `x` to the left.
        Args:
            x (AVLNode): The node to be rotated.
        Returns:
            AVLNode: The new root of the subtree after rotation.
        """

        #current = current node just added to the tree        
        current = x.right #current > x
        t2 = current.left #T2 < current and T2 > x
        
        #rotation: now current will be the root of the tree
        current.left = x
        x.right = t2 

        #update heights
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        current.height =  1 + max(self._height(current.left), self._height(current.right))

        return current


    def _insert_recursive(self, current: Optional[AVLNode], key: Any, value: Any) -> AVLNode:
        """
        Recursively inserts a new node with the given key and value into the AVL tree.
        Args:
            current (Optional[AVLNode]): The current node being considered during the recursive insertion.
            key (Any): The key of the new node.
            value (Any): The value of the new node.
        Returns:
            AVLNode: The updated AVL tree with the new node inserted.
        """

        #normal binary tree to insert the node
        if not current:
            node = AVLNode(key)
            node.add_value(value)
            return node
        current = super()._insert_recursive(current, key, value)
        
        current.height = 1 + max(self._height(current.left), self._height(current.right)) #update height of tree @ current node
        balance_factor = self._height(current.left) - self._height(current.right)  #find balance factor @ current node

        #determine if any rotations of the tree with the newly added node are needed based on the above calculated balance factor:
        #1. too many nodes inserted to the left (LL and LR cases):
        if balance_factor >= 2:    
            if key < current.left.key: #LL
                return self._rotate_right(current)
            elif current.key > current.left.key: #LR 
                current.left = self._rotate_left(current.left)
                return self._rotate_right(current) 
            else: current.left.add_value(value)

        #2. too many nodes inserted to the right (RR and RL cases):
        elif balance_factor <= -2:
            if key > current.right.key: #RR
                return self._rotate_left(current)
            elif key < current.right.key: #RL
                current.right = self._rotate_right(current.right)
                return self._rotate_left(current)
            else: current.right.add_value(value)
        else:
            return current
        

    def insert(self, key: Any, value: Any) -> None:
        """
        Inserts a key-value pair into the AVL tree. If the key exists, the
         value will be appended to the list of values in the node. 

        Parameters:
            key (Any): The key to be inserted.
            value (Any): The value associated with the key.

        Returns:
            None
        """
        if self.root is None:
            self.root = AVLNode(key)
            self.root.add_value(value)
        else:
            super().insert(key, value)


    def _inorder_traversal(self, current: Optional[AVLNode], result: List[Any]) -> None:
         if current is None:
             return
        
         self._inorder_traversal(current.left, result)
         result.append(current.key)
         self._inorder_traversal(current.right, result)

   
    # def get_keys(self) -> List[Any]:
    #     keys: List[Any] = [] 
    #     self._inorder_traversal(self.root, keys)
    #     return keys
    

