from indexer.abstract_index import AbstractIndex
import hashlib

class HashMapIndex(AbstractIndex):
    
    def __init__(self, size=500000):
        super().__init__()
        # self.hash_map = {} 
        self.bucket_size = size 
        self.buckets = [None for _ in range(self.bucket_size)] # used Nones since I wasn't sure if I could generate empty tuples to hold space in the table
        self.num_occupied = 0 # to keep track of non-None elements of the hash table for resizing purposes
        
    def __iter__(self): # how to iterate/traverse through the hash map
        for element in self.buckets:
            for k,v in element:  # each bucket contains (term, [doc_ids])
                yield k
                
    def __resize__(self): # makes the table bigger if necessary
        self.buckets.extend([None] * self.bucket_size) # doubles the size of the table 
        self.bucket_size = len(self.buckets) # updates the size of the table to reflect the doubling
        
    def hash_function(self,term):
        pos_hex = hashlib.sha256(term.encode("utf-8"))
        pos = int(pos_hex.hexdigest(), 16) % self.bucket_size
        return pos   

    def insert(self, term, document_id):
        pos = self.hash_function(term)
        
        if self.buckets[pos] is not None and self.buckets[pos][0] == term: #if the word is already in the table, add the file to that word's doc list
            if document_id not in self.buckets[pos][1]:
                self.buckets[pos][1].append(document_id) 
        else:
           self.buckets[pos] = (term, [document_id]) # if the word isn't indexed already replace the None with (term, [doc_ids]) 
           self.num_occupied += 1 # update the occupancy counter
        
        if self.num_occupied / self.bucket_size > 0.9:
            self.__resize__() # if the occupancy of the table is over 90%, resize the table

    def search(self, term):
        pos = self.hash_function(term) # the position where we expect to find this word
        if self.buckets[pos] is not None: # if the word is indexed, return it's doc list
            k,v = self.buckets[pos]
            if k == term:
              return v
        return None
    
    def get_keys_in_order(self):
        keys = []
        for element in self.buckets: 
            if element is not None:
                k,v = element 
                keys.append(k)
        return sorted(keys)
    
    def count_keys(self) -> int:
        return len(self.get_keys_in_order())
    
    def get_avg_value_list_len(self):
        element_lens = []
        list_len_sum = 0
        num_keys = 0
        for element in self.buckets:
            if element is not None:
                element_lens.append(len(element[1]))
                list_len_sum += len(element[1])
                num_keys += 1  
        return (list_len_sum / num_keys), element_lens 


