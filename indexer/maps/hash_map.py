from indexer.abstract_index import AbstractIndex
import hashlib

class HashMapIndex(AbstractIndex):
    
    def __init__(self, size=500000):
        super().__init__()
        # self.hash_map = {} 
        self.bucket_size = size 
        self.buckets = [None for _ in range(self.bucket_size)]
        
    def __iter__(self):
        for element in self.buckets:
            for k,v in element:  # Each bucket contains (term, [doc_ids])
                yield k
        
    def hash_function(self,term):
        pos_hex = hashlib.sha256(term.encode("utf-8"))
        pos = int(pos_hex.hexdigest(), 16) % self.bucket_size
        return pos   

    def insert(self, term, document_id):
        pos = self.hash_function(term)
        
        if self.buckets[pos] is not None and self.buckets[pos][0] == term:
            self.buckets[pos][1].append(document_id)
        else:
           self.buckets[pos] = (term, [document_id])  

    def search(self, term):
        pos = self.hash_function(term)
        if self.buckets[pos] is not None:
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
        list_len_sum = 0
        num_keys = 0
        for element in self.buckets:
            list_len_sum += len(element[1])
            num_keys += 1  
        return (list_len_sum / num_keys)


