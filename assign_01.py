import os
import argparse 
import json
import uuid
from urllib.parse import urlparse
from typing import *
from indexer.trees.avl_tree import AVLTreeIndex
from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.maps.hash_map import HashMapIndex
from indexer.arrays.array import SortedArrayIndex
from indexer.util.timer import timer
from indexer.abstract_index import AbstractIndex
from utils.exp2csv import log_timing_data
from utils.expsets import generate_experiment_datasets
from indexer.util.pickle_utils import save_index_to_pickle, load_index_from_pickle


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
                search_times.append(time_ns_1 + time_ns_2 + time_ns_3)
    
            elif word_count == 2:
                r1, time_ns_1 = timed_search(index, split_words[0])
                r2, time_ns_2 = timed_search(index, split_words[1])
                result = list(set(r1) & set(r2))  # find common docs
                search_times.append(time_ns_1 + time_ns_2)
    
            else:  # single-word case
                result, time_ns = timed_search(index, word)  
                search_times.append(time_ns)  
    
            if result:
                valid_kvs[word] = result 
            else:
                continue

    return valid_kvs, search_times  # return results and timing data
                


def main():
    # initialize argument parser
    parser = argparse.ArgumentParser(description="Index news articles using different data structures.")
    
    # setting up the command-line arguments
    parser.add_argument(
        '-d', '--dataset', 
        type=str, 
        help="Path to the root folder of the dataset."
    ) # when running from terminal we can now do python assign_01.py -d path.json to pass the dataset
    
    parser.add_argument(
        '-p', '--pickle', 
        type=str, 
        help="Path to the pickle file for saving or loading the index."
    ) # when constructing an new index structure we can save to a pickle by doing python assign_01.py -d path.json -p index.pkl
    
    parser.add_argument(
        '--load', 
        action='store_true', 
        help="Load the index from the pickle file instead of creating a new one."
    ) # when referring to/running experiments for an index structure that is already constructed we can do python assign_01.py --load -p index.pkl
    
    # saves info passed into terminal run command
    args = parser.parse_args()
    
    # loads whichever index file is specified if --load command is used 
    if args.load:
        if args.pickle:
            index = load_index_from_pickle(args.pickle)
            print("Select the indexing structure you loaded:")
            print("1 - Binary Search Tree (BST)")
            print("2 - AVL Tree")
            print("3 - Hash Table")
            print("4 - Array")
            choice = input("Enter the number corresponding to your choice: ").strip()
        
            # just for record-keeping purposes
            if choice == "1":
                choice = "BST"
            elif choice == "2":
                choice = "AVL"
            elif choice == "3":
                choice = "Hash"
            elif choice == "4":
               choice = "Array"
            else:
                print("Invalid choice.")
        else:
            print("Error: --load requires a --pickle argument.")
    else:
       # asks which index structure the user wants to construct if they don't choose to load a pickle file
        print("Select an indexing structure:")
        print("1 - Binary Search Tree (BST)")
        print("2 - AVL Tree")
        print("3 - Hash Table")
        print("4 - Array")
        choice = input("Enter the number corresponding to your choice: ").strip()
    
        # construct the selected index
        if choice == "1":
            choice = "BST"
            index = BinarySearchTreeIndex()
        elif choice == "2":
            choice = "AVL"
            index = AVLTreeIndex()
        elif choice == "3":
            choice = "Hash"
            index = HashMapIndex()
        elif choice == "4":
           choice = "Array"
           index = SortedArrayIndex()
        else:
            print("Invalid choice.")
    
        # constructs whichever index structure is indicated
        if args.dataset:
            index_files(args.dataset, index)
        else:
            print("Error: --dataset argument is required for indexing.")
    
        # saves new index structure to a pickle file with whatever name was provided in the terminal
        if args.pickle:
            save_index_to_pickle(index, args.pickle)

    # As a gut check, we are printing the keys that were added to the
    # index in order
    print(index.get_keys_in_order())
    tokens = len(index.get_keys_in_order())
    
    """
    
    for i in range(10): 
        datasets, n = generate_experiment_datasets(index)
        for dataset in datasets:
            log_timing_data(
                index_type=choice,
                uid=uuid.uuid1(), 
                num_docs=306242, 
                num_tokens=tokens, 
                search_set_size=n, 
                search_function=search,
                index=index,
                search_set = dataset
            )

"""       
    


if __name__ == "__main__":
    main()
