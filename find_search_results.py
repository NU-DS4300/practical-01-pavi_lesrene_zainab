#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 04:16:47 2025

@author: lesrene
"""

# Only here to create the list of documents we need to return for the specified search set

import os
import json
from urllib.parse import urlparse
from typing import *
from indexer.abstract_index import AbstractIndex
from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.maps.hash_map import HashMapIndex
from indexer.util.timer import timer

# turns a string into list of tokens
# will be used to turn title & author names into processed text
def tokenize(text: str): #-> List[str]:
    if not text: 
        return [] # gives us an empty list if no text is provided
    text = text.lower() # converts the text to lowercase
    tokens = text.split() # splits the text by whitespace so each word is a token
    cleaned_tokens = [''.join(char for char in token if char.isalnum()) for token in tokens] # keeps only alphanumeric characters from each token
    return [token for token in cleaned_tokens if token] # filters out empty tokens (which could happen if there were non-alphanumeric-only inputs)

# parses a json file
def process_file(json_data: Dict[str, Any]) -> Dict[str, Any]:
    title = json_data.get("title")
    full_url = json_data.get("url")
    if full_url:
        domain_url = urlparse(full_url).netloc # source: ChatGPT, this made it easier to get the domain by identifying the network location
    author = json_data.get("author")
    preprocessed_text = json_data.get("preprocessed_text")
    # tokenize title and add to preprocessed_text
    title_tokens = tokenize(title)
    preprocessed_text.extend(title_tokens)
    # tokenize author last name (if present) and add to preprocessed_text
    if author:
        author_tokens = tokenize(author)
        preprocessed_text.extend(author_tokens)
        
    return {
        "title": title,
        "url": domain_url,
        "author": author,
        "preprocessed_text": preprocessed_text
    }

# crawls through files in the path, extracts metadata, and indexes them into the particular index structure
def index_files(path: str, index: AbstractIndex) -> None:
    if path is not None:
        print(f"path = {path}") # as long as the directory actually exists this should print, just a sanity check

    for root, subs, files in os.walk(path): # recursively go through the directory 
        for file in files: 
            if file.endswith('.json'):  # only for the .json files just in case, also just sanity check
                file_path = os.path.join(root, file) # does: /top_folder/wtv_sub_folder(s) += /filename.json
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        json_data = json.load(f) # reads json file
                        metadata = process_file(json_data) # parses into python dictionary with relevant info
                        for word in set(metadata["preprocessed_text"]): # only indexes the unique words just for convenience
                            index.insert(word, file) # insert the k,v into the index structure
                    except json.JSONDecodeError: # source: ChatGPT for if the json couldn't be read for troubleshooting
                        print(f"Error decoding JSON in file: {file_path}")
                        
                       
def timed_search(index, word):
    # just here so we can time the search for each word 
    @timer
    def search_word():
        return index.search(word)

    result, time_ns = search_word()  # gets both result and execution time
    return result, time_ns  

def search(index, search_set):
    valid_kvs = {}
    search_times = [] 
    
    for dataset in search_set:
        for word in dataset:
            word = word.lower()
            split_words = word.split()
            word_count = len(split_words)  
    
            if word_count == 3:
                r1, time_ns_1 = timed_search(index, split_words[0])
                r2, time_ns_2 = timed_search(index, split_words[1])
                r3, time_ns_3 = timed_search(index, split_words[2])
                result = list(set(r1) & set(r2) & set(r3))  # finds common docs

    
            elif word_count == 2:
                r1, time_ns_1 = timed_search(index, split_words[0])
                r2, time_ns_2 = timed_search(index, split_words[1])
                result = list(set(r1) & set(r2))  # find common docs
    
            else:  # single-word case
                result, time_ns = timed_search(index, word) 
    
            if result:
                valid_kvs[word] = result 
            else:
                continue

    return valid_kvs, search_times  # return results and timing data


def main():
    data_directory = "/Users/lesrene/Downloads/P01-verify-dataset"

    hash_index = HashMapIndex()
    index_files(data_directory, hash_index)
    print(hash_index.get_keys_in_order())
    
    test_words = ['Northeastern', 'Beanpot', 'Husky']
    pretend_dataset = [test_words]
    search_results, _ = search(hash_index, pretend_dataset)
    
    with open("search_results.json", "w") as file:
        json.dump(search_results, file)  
    

if __name__ == "__main__":
    main()