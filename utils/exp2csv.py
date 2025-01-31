#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 23:46:45 2025

@author: lesrene
"""

import csv
import os
import numpy as np

CSV_FILENAME = "timing_data.csv"

COMPUTE_PROC_TYPE = "Apple M1"
PRIMARY_MEMORY_SIZE = 8


def log_timing_data(index_type, uid, num_docs, num_tokens, search_set_size,search_function,index,search_set):
    run_id = uid

    results, search_times = search_function(index,search_set)
    search_time = np.sum(search_times)
    

    data = [
        run_id, COMPUTE_PROC_TYPE, PRIMARY_MEMORY_SIZE, index_type, 
        num_docs, num_tokens, search_set_size, search_time
    ]

    file_exists = os.path.exists(CSV_FILENAME)

    with open(CSV_FILENAME, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        # add header if the file is newly created
        if not file_exists:
            writer.writerow([
                "run_id", "compute_proc_type", "primary_memory_size", 
                "index_type", "num_docs_indexed", "num_tokens_indexed", 
                "search_set_base_size", "search_time"
            ])

        writer.writerow(data)  # add row with experiment data

