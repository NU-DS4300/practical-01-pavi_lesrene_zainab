#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 01:00:40 2025

@author: lesrene
"""
from typing import *
import random
from indexer.abstract_index import AbstractIndex
import string

# generates a random n that is a multiple of 4 and is greater than or equal to 4000
def generate_n(seed=42): #-> int
    random.seed(seed) # makes sure that we always get the same random number so that datasets of the same sizes are always created
    return random.randint(1000, 10000) * 4 

# generates the search datasets made up of the A,B,C,D components that were asked of us in the assignment 
# might make a seperate file to run this function (and generate_n function) and save the search datasets (x10 loop) and import search datasets in the beginning
def generate_search_data(index: AbstractIndex, n: int): #-> List[str]
    # gets all the keys from the index structure
    keys = index.get_keys_in_order()  # *note to whoever implements AVL: get_keys method should return the keys sorted # let's only give it BST
    if not keys: # sanity check just in case the indexing didn't work and the index structure has no k,v pairs
        print("Index is empty; cannot generate search data.")
        return []

    component_a = random.sample(keys, n) # gets a random sample of n keys list (so words that are def in the structure)

    component_b = [' '.join(random.sample(component_a, random.choice([2, 3]))) for _ in range(n // 4)] # chooses sometimes 2, sometimes 3 (through random.choice) words from component a (through random.sampling) to make up n//4 'phrases' 

    component_c = [''.join(random.choices(string.ascii_letters, k=10)) for _ in range(n)] # randomly selects 10 characters from the set of uppercase & lowercase alphabet to form n fake words

    component_d = [' '.join(random.sample(component_c, random.choice([2, 3]))) for _ in range(n // 4)] # # chooses sometimes 2, sometimes 3 (through random.choice) words from component c (through random.sampling) to make up n//4 phrases 

    # combine and shuffle these sets
    search_data_set = component_a + component_b + component_c + component_d
    random.shuffle(search_data_set)
    return search_data_set

def generate_experiment_datasets(index: AbstractIndex): #-> List[List[str]]
    datasets = [] 
    for i in range(10): # assignment asked that we make 8 or more search datasets
        n = generate_n(seed=42+i) 
        dataset = generate_search_data(index, n)
        datasets.append(dataset)
    return datasets, n
