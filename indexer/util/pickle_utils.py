#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 00:56:32 2025

@author: lesrene
"""

import pickle
from typing import *
from indexer.abstract_index import AbstractIndex

def save_index_to_pickle(index: AbstractIndex, pickle_path: str):
    with open(pickle_path, 'wb') as f:
        pickle.dump(index, f)
    print(f"Index saved to {pickle_path}")


def load_index_from_pickle(pickle_path: str) -> AbstractIndex:
    with open(pickle_path, 'rb') as f:
        index = pickle.load(f)
    print(f"Index loaded from {pickle_path}")
    return index