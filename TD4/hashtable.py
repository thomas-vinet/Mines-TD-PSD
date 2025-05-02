from __future__ import annotations
import matplotlib.pyplot as plt
        
#Les fonctions de hachages utilisées dans le TP

def naive_hash(string: str) -> int:
    return sum([ord(c) for c in string])

def hashcode(string: str) -> int:
    h = 0
    for v in string:
        h = 31*h + ord(v)
    return h

def jenkins(string: str) -> int:
    hash = 0
    for c in string:
        hash += ord(c)
        hash += hash << 10
        hash ^= hash >> 6
    hash += hash << 3
    hash ^= hash >> 11
    hash += hash << 15
    return hash


class HashTable:

    def __init__(self, hash_function: callable[str, int], size = 16):
        self.hash_function = hash_function
        self.size = size
        self.table = [None] * self.size
        self.elements = 0

    def put(self, key: str, value):
        index = self.hash_function(key) % self.size
        if self.table[index] == None:
            self.table[index] = [[key, value]]
            self.elements += 1
        else:
            for pair in self.table[index]:
                if pair[0] == key:
                    pair[1] = value
                    return
            self.table[index].append([key, value])
            self.elements += 1
        #if self.elements > 1.2 * self.size:
        #    self.resize(self.size)

    def get(self, key: str):
        index = self.hash_function(key) % self.size
        if self.table[index] == None:
            return None
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        return None
    
    def repartition(self):
        x = range(self.size)
        y = [len(t) if t != None else 0 for t in self.table]
        width = 1/1.5
        plt.bar(x, y, width, color="blue")
        plt.show()

    def resize(self, new_size):
        new_table = [None] * new_size
        for t in self.table:
            if t == None:
                continue
            for pair in t:
                k, v = pair
                index = self.hash_function(k) % new_size
                if new_table[index] == None:
                    new_table[index] = [[k, v]]
                else:
                    new_table[index].append([k, v])
        self.table = new_table
        self.size = new_size
    


def french_histogram(N = 320):
    ht = HashTable(naive_hash, N)
    #ht = HashTable(jenkins, N)
    file = open("frenchssaccent.dic", "r")
    for line in file.readlines():
        mot = line.strip()
        size = len(mot)
        ht.put(mot, size)
    ht.repartition()
    
if __name__ == "__main__":
    ht = HashTable(naive_hash)
    ht.put('abc', 3)
    assert ht.get('aaa') == None
    assert ht.get('abc') == 3
    ht.put('abc', 5)
    assert ht.get('abc') == 5
    french_histogram()