import os
import json
import random

class TrieNode:
    def __init__(self):
        """Initializes a Trie node with empty children and a set of documents."""
        self.children = {}
        self.documents = set()

class TrieIndexer:
    def __init__(self):
        """Initializes a Trie indexer with a root TrieNode."""
        self.root = TrieNode()
    
    def insert(self, word, document):
        """Inserts a word into the Trie and associates it with a document."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.documents.add(document)
    
    def search(self, word):
        """Searches for a word in the Trie and returns the set of documents it appears in."""
        node = self.root
        for char in word:
            if char not in node.children:
                return set()  # Word not found
            node = node.children[char]
        return node.documents

    def index_documents(self, directory):
        """Traverses the directory, reads JSON files, and indexes preprocessed text."""
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    if "preprocessed_text" in data:
                        for word in data["preprocessed_text"]:
                            self.insert(word, filename)
