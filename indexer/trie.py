import os
import json
from urllib.parse import urlparse
from typing import List, Set

class TrieNode:
    def __init__(self):
        self.children = {}
        self.documents = set()  # Using set for O(1) lookups

class TrieIndexer:
    def __init__(self):
        self.root = TrieNode()
        self._case_sensitive = False  # Configurable option

    def _normalize(self, word: str) -> str:
        """Normalize word based on case sensitivity setting"""
        return word if self._case_sensitive else word.lower()

    def insert(self, word: str, document: str) -> None:
        """Insert case-normalized word with document association"""
        node = self.root
        for char in self._normalize(word):
            node = node.children.setdefault(char, TrieNode())
        node.documents.add(document)

    def search(self, word: str) -> List[str]:
        """Return sorted list of documents for normalized word"""
        node = self.root
        for char in self._normalize(word):
            if char not in node.children:
                return []
            node = node.children[char]
        return sorted(list(node.documents))  # Consistent return type

    def _extract_metadata(self, data: dict) -> List[str]:
        """Extract required metadata tokens"""
        tokens = []
        
        # 1. Title words
        if title := data.get("title"):
            tokens.extend(title.split())
        
        # 2. Source domain
        if url := data.get("url"):
            domain = urlparse(url).netloc
            tokens.append(domain)
        
        # 3. Author last name
        if author := data.get("author"):
            if " " in author:
                tokens.append(author.split()[-1])
        
        return tokens

    def index_documents(self, root_dir: str) -> None:
        """Recursively process all JSON files in directory structure"""
        for root, _, files in os.walk(root_dir):
            for filename in files:
                if filename.endswith(".json"):
                    path = os.path.join(root, filename)
                    with open(path, "r", encoding="utf-8") as f:
                        try:
                            data = json.load(f)
                            
                            # Index preprocessed text
                            if "preprocessed_text" in data:
                                for word in data["preprocessed_text"]:
                                    self.insert(word, filename)
                            
                            # Index metadata tokens
                            for token in self._extract_metadata(data):
                                self.insert(token, filename)
                                
                        except json.JSONDecodeError:
                            print(f"Error parsing {filename}")
