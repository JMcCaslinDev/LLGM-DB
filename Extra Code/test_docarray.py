import unittest
import numpy as np
from item_doc import ItemDoc

class TestItemDoc(unittest.TestCase):

    def test_item_doc(self):
        item_doc = ItemDoc(
            name="Iron Sword",
            type="Weapon",
            properties="A dull iron sword"
        )

        # Assuming your ItemDoc class embeds the input strings during initialization
        # and calculates the document-level embedding
        # You can add your implementation details here

        # Print the first 5 elements of each embedding
        print("Name Embedding (First 5 elements):", item_doc.name['embedding'][:5])
        print("Type Embedding (First 5 elements):", item_doc.type['embedding'][:5])
        print("Properties Embedding (First 5 elements):", item_doc.properties['embedding'][:5])
        # Uncomment this block if you decide to handle doc_embedding
        # print("Document Embedding (First 5 elements):", item_doc.doc_embedding[:5])

        # Assertions to check if embeddings are generated
        self.assertIsNotNone(item_doc.name['embedding'])
        self.assertIsNotNone(item_doc.type['embedding'])
        self.assertIsNotNone(item_doc.properties['embedding'])
        # Uncomment this line if you decide to handle the doc_embedding
        # self.assertIsNotNone(item_doc.doc_embedding)

if __name__ == '__main__':
    unittest.main()
