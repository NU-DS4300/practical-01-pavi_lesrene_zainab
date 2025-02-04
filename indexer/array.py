import os
import json
import bisect
from urllib.parse import urlparse
from typing import List, Tuple, Dict

class SortedArrayIndexer:
    """
    Array-based inverted index using binary search for lookups.
    Sorted array of (word, documents) tuples.
    Does metadata extraction.
    """
    
    def __init__(self, case_sensitive: bool = False):
        self._case_sensitive = case_sensitive
        self._array = []        # Main storage: [(word, [doc_ids])]
        self._words = []        # Parallel array for bisect operations
        self.metadata = {}      # {filename: {title, domain, author}}
        self.stats = {
            'num_docs': 0,
            'num_tokens': 0
        }

    def _normalize(self, word: str) -> str:
        """Handle cases"""
        return word if self._case_sensitive else word.lower()

    def insert(self, word: str, document: str) -> None:
        """Use sorted array with O(log n) search + O(n) insertion"""
        if not word:
            return

        norm_word = self._normalize(word)

        # Find insertion point using binary search
        idx = bisect.bisect_left(self._words, norm_word)
        
        if idx < len(self._words) and self._words[idx] == norm_word:
            # Existing word - append document if new
            if document not in self._array[idx][1]:
                self._array[idx][1].append(document)
        else:
            # New word - insert at position
            self._words.insert(idx, norm_word)
            self._array.insert(idx, (norm_word, [document]))
            self.stats['num_tokens'] += 1

    def search(self, word: str) -> List[str]:
        """Binary search implementation with O(log n) complexity"""
        norm_word = self._normalize(word)
        idx = bisect.bisect_left(self._words, norm_word)
        
        if idx < len(self._words) and self._words[idx] == norm_word:
            return self._array[idx][1]
        return []

    def _extract_metadata(self, data: dict) -> List[str]:
        """Extract metadata tokens"""
        tokens = []
        
        # Title processing (Component A)
        if title := data.get('title'):
            tokens.extend(title.split())
        
        # Domain extraction (Component B)
        if url := data.get('url'):
            domain = urlparse(url).netloc
            if domain:
                tokens.append(domain)

        # Author processing (Component C)
        if author := data.get('author'):
            if ' ' in author:
                tokens.append(author.split()[-1])
        
        return tokens

    def index_documents(self, root_dir: str) -> None:
        """Recursive directory processing with metadata"""
        self.stats['num_docs'] = 0
        seen_docs = set()
        
        for root, _, files in os.walk(root_dir):
            for filename in files:
                if not filename.endswith('.json'):
                    continue
                
                path = os.path.join(root, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        seen_docs.add(filename)
                        
                        # Store metadata
                        self.metadata[filename] = {
                            'title': data.get('title', ''),
                            'domain': urlparse(data.get('url', '')).netloc,
                            'author': data.get('author', '')
                        }
                        
                        # Index preprocessed text
                        if 'preprocessed_text' in data:
                            for word in data['preprocessed_text']:
                                self.insert(word, filename)
                        # Index metadata tokens
                        for token in self._extract_metadata(data):
                            self.insert(token, filename)
                            
                    except json.JSONDecodeError:
                        print(f"Error parsing {filename}")
        
        self.stats['num_docs'] = len(seen_docs)

    def get_index_size(self) -> int:
        """Return total number of indexed tokens"""
        return self.stats['num_tokens']
