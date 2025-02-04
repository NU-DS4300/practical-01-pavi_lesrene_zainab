from indexer.abstract_index import AbstractIndex
import bisect

class SortedArrayIndex(AbstractIndex):
    """
    Array-based inverted index using binary search for lookups.
    Stores words in a sorted array and maintains a list of associated documents.
    """
    
    def __init__(self):
        self._array = []        # [(word, [doc_ids])]
        self._words = []        # just the words (in the same order) so we can do the bisect 
    
    def insert(self, word: str, document: str) -> None:
        # uses binary search to find where to put the word alphabetically
        idx = bisect.bisect_left(self._words, word) 
        
        if idx < len(self._words) and self._words[idx] == word: # idx < len(self._words) used to avoid IndexError
            # if the word already exists add the document to it's docs list
            if document not in self._array[idx][1]:
                self._array[idx][1].append(document)
        else:
            # adds new word at the correct position alphabetically to words array and to the k,v array
            self._words.insert(idx, word)
            self._array.insert(idx, (word, [document]))
    
    def search(self, word: str):
        # uses binary search to find where we expect to find the word alphabetically
        idx = bisect.bisect_left(self._words, word)
        
        if idx < len(self._words) and self._words[idx] == word:
            return self._array[idx][1] # if the word is indexed, return it's doc list
        return []
    
    def __iter__(self):
        for word, docs in self._array:
            yield word
    
    def get_keys_in_order(self):
        """Returns all indexed words in sorted order."""
        return self._words
