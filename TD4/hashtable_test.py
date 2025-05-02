import unittest
from hashtable import HashTable, hashcode, naive_hash

class HashTableTest(unittest.TestCase):

    def testNone(self):
        ht = HashTable(hashcode)
        self.assertIsNone(ht.get("aaa"))

    def testputget(self):
        ht = HashTable(hashcode)
        ht.put("abc", 5)
        self.assertEqual(ht.get("abc"), 5)

    def testupdate(self):
        ht = HashTable(hashcode)
        ht.put("abc", 5)
        self.assertEqual(ht.get("abc"), 5)
        ht.put("abc", 3)
        self.assertEqual(ht.get("abc"), 3)

    def testmultiples(self):
        ht = HashTable(hashcode)
        char = [chr(65+i) + chr(65+(i+1)%26) for i in range(26)]
        for i, v in enumerate(char):
            ht.put(v, i)
        for i, v in enumerate(char):
            self.assertEqual(ht.get(v), i)

    def testResize(self):
        ht = HashTable(hashcode, 1000)
        ht2 = HashTable(hashcode, 500)
        char = [chr(65+i) + chr(65+(i+1)%26) for i in range(26)]
        for i, v in enumerate(char):
            ht.put(v, i)
            ht2.put(v, i)
        ht.resize(2000)
        for i, v in enumerate(char):
            self.assertEqual(ht.get(v), ht2.get(v)) 
        

    def testcollision(self):
        ht = HashTable(naive_hash)
        ht.put("abc", 3)
        ht.put("cba", 5)
        ht.put("abc", 7)
        self.assertEqual(ht.get("abc"), 7)
        self.assertEqual(ht.get("cba"), 5)

if __name__ == "__main__":
    unittest.main()

