import bisect

class SortedArrayIndexer:
    """
    Array-based inverted index using binary search for lookups.
    Stores words in a sorted array and maintains a list of associated documents.
    """
    
    def __init__(self):
        self._array = []        # [(word, [doc_ids])]
        self._words = []        # Parallel array for bisect operations
    
    def insert(self, word: str, document: str) -> None:
        """Use binary search for O(log n) lookups and O(n) insertions."""
        if not word:
            return

        # Find insertion point using binary search
        idx = bisect.bisect_left(self._words, word)
        
        if idx < len(self._words) and self._words[idx] == word:
            # Existing word - append document if new
            if document not in self._array[idx][1]:
                self._array[idx][1].append(document)
        else:
            # New word - insert at position
            self._words.insert(idx, word)
            self._array.insert(idx, (word, [document]))
    
    def search(self, word: str):
        """Binary search implementation with O(log n) complexity."""
        idx = bisect.bisect_left(self._words, word)
        
        if idx < len(self._words) and self._words[idx] == word:
            return self._array[idx][1]
        return []
    
    def __iter__(self):
        """Allows iteration over the index in sorted order."""
        for word, docs in self._array:
            yield word, docs
    
    def get_keys_in_order(self):
        """Returns all indexed words in sorted order."""
        return self._words
