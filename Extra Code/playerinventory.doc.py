from docarray.typing import NdArray
from typing import List
from item_doc import ItemDoc
from docarray.base_doc import BaseDoc  # Import BaseDoc if it's in a separate file
from variable_embedding_pair import VariableEmbeddingPair  # Import VariableEmbeddingPair class
import numpy as np
from openai_helper import generate_embedding  # Import the helper function

class PlayerInventory(BaseDoc):
    #   List of ItemDocs in the Player Inventory
    items: List[ItemDoc] = []  
    
    #   Using VariableEmbeddingPair for character name and ID
    character_name = VariableEmbeddingPair(1536)
    character_id = VariableEmbeddingPair(1536)

    #   Overall embedding for the Player Inventory
    doc_embedding: NdArray[1536]  


    def update_embeddings(self, model: str = "text-embedding-ada-002"):
        all_embeddings = []
        
        # Update embeddings for individual items in the inventory
        for item in self.items:
            item.update_embeddings(model)
            all_embeddings.append(item.doc_embedding)
        
        # Update embeddings for character name and ID
        for attribute in ['character_name', 'character_id']:
            pair = getattr(self, attribute)
            if pair.variable:
                embedding_list = generate_embedding(pair.variable, model)
                if embedding_list:
                    pair.set_embedding(np.array(embedding_list))
                    all_embeddings.append(embedding_list)

        if all_embeddings:
            self.embedding = np.mean(np.array(all_embeddings), axis=0)
