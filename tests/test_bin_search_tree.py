#numbers should be bigger than this:
#both trees 260,000 unique keys (nodes)
#AVL tree height 21
#AVL tree built in 178 sec
#average link of lists of documents for which word appears = 268

"""
This module contains unit tests for the BinarySearchTreeIndex class.

The BinarySearchTreeIndex class is responsible for implementing a binary search tree index for a search engine.
The following tests are included:
- `test_insert_and_search`: Tests the `insert` and `search` methods of the BinarySearchTreeIndex class.
- `test_insert_duplicate_keys`: Tests the behavior of inserting duplicate keys into the BinarySearchTreeIndex class.
- `test_search_non_existent_key`: Tests the behavior of searching for a non-existent key in the BinarySearchTreeIndex class.
- `test_count_nodes`: Tests the `count_nodes` method of the BinarySearchTreeIndex class.
- `test_tree_height`: Tests the `tree_height` method of the BinarySearchTreeIndex class.
- `test_get_keys_in_order`: Tests the `get_keys_in_order` method of the BinarySearchTreeIndex class.
- `test_get_leaf_keys`: Tests the `get_leaf_keys` method of the BinarySearchTreeIndex class.
"""
import pytest
from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.trees.bst_node import BSTNode
from indexer.trees.avl_node import AVLNode
from indexer.trees.avl_tree import AVLTreeIndex

#AVL tests:
@pytest.fixture
def avl():
  return AVLTreeIndex()

def test_insert_and_search_avl(avl):
  avl.insert('d', 4)
  avl.insert('e', 5)
  avl.insert('f', 6) 

  assert avl.search('d') == [4]
  assert avl.search('e') == [5]
  assert avl.search('f') == [6]

def test_count_nodes_avl(avl):
  avl.insert('d', 4)
  avl.insert('e', 5)
  avl.insert('f', 6)
  
  assert avl.count_nodes() == 3

def test_tree_height_avl(avl):
  avl.insert('d', 4)
  avl.insert('e', 5)
  avl.insert('f', 6)
  
  assert avl.tree_height() == 2

def test_get_keys_in_order_avl(avl):
  avl.insert('d', 4)
  avl.insert('e', 5)
  avl.insert('f', 6)

  assert avl.get_keys_in_order() == ['d', 'e', 'f']

def test_get_leaf_keys_avl(avl):
  avl.insert('d', 4)
  avl.insert('e', 5)
  avl.insert('f', 6)
  
  assert avl.get_leaf_keys() == ['d', 'f']


#BST tests:
@pytest.fixture
def bst():
  return BinarySearchTreeIndex()

def test_insert_and_search(bst):
  bst.insert('a', 1)
  bst.insert('b', 2)
  bst.insert('c', 3)
  
  assert bst.search('a') == [1]
  assert bst.search('b') == [2]
  assert bst.search('c') == [3]

def test_insert_duplicate_keys(bst):
  bst.insert('a', 1)
  bst.insert('a', 2)
  bst.insert('a', 3)
  
  assert bst.search('a') == [1, 2, 3]

def test_search_non_existent_key(bst):
  bst.insert('a', 1)
  
  with pytest.raises(KeyError):
    bst.search('b')

def test_count_nodes(bst):
  bst.insert('a', 1)
  bst.insert('b', 2)
  bst.insert('c', 3)
  
  assert bst.count_nodes() == 3

def test_tree_height(bst):
  bst.insert('a', 1)
  bst.insert('b', 2)
  bst.insert('c', 3)
  
  assert bst.tree_height() == 3

def test_get_keys_in_order(bst):
  bst.insert('b', 2)
  bst.insert('a', 1)
  bst.insert('c', 3)
  
  assert bst.get_keys_in_order() == ['a', 'b', 'c']

def test_get_leaf_keys(bst):
  bst.insert('b', 2)
  bst.insert('a', 1)
  bst.insert('c', 3)
  
  assert bst.get_leaf_keys() == ['a', 'c']


if __name__ == "__main__":
  pytest.main()
