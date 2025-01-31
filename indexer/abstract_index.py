from typing import List, Optional, Any, Generator
from abc import ABC, abstractmethod

from indexer.trees.bst_node import BSTNode


class AbstractIndex(ABC):
    def __init__(self):
       self.values: List[Any] = []
       self.left: Optional['BSTNode'] = None
       self.right: Optional['BSTNode'] = None


    @abstractmethod
    def insert(self, key: Any, value: Any) -> None:
        self.root = self._insert_recursive(self.root, key, value)


    @abstractmethod
    def search(self, key: Any) -> List[Any]:
        return self._search_recursive(self.root, key)

    @abstractmethod
    def __iter__(self) -> Generator[Any, None, None]:
        yield from self._inorder_traversal_generator(self.root)

