from docarray import BaseDoc
from docarray.typing import NdArray
from openai_helper import generate_embedding  # Import the helper function
import numpy as np
from pydantic import root_validator, BaseModel
from numpy import ndarray

class ItemDocConfig:
    arbitrary_types_allowed = True

class ItemDoc(BaseDoc):
    class Config(ItemDocConfig):
        pass

    name: str
    type: str
    description: str

    name_embedding: ndarray[(1536,)] = None
    type_embedding: ndarray[(1536,)] = None
    description_embedding: ndarray[(1536,)] = None
    doc_embedding: ndarray[(1536,)] = None

    @root_validator(pre=False, skip_on_failure=True)
    def generate_and_store_embeddings(cls, values):
        name, type_, description = values.get('name'), values.get('type'), values.get('description')

        # Generate embeddings for each field
        values['name_embedding'] = generate_embedding(name)
        values['type_embedding'] = generate_embedding(type_)
        values['description_embedding'] = generate_embedding(description)

        # Generate combined string
        combined_string = f"ItemDoc: Name: {name}, Type: {type_}, Description: {description}"

        # Generate the overall document embedding
        values['doc_embedding'] = generate_embedding(combined_string)

        return values



    def print_item_doc(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
            print("\n")

    # #   Moved from pinecone_helper.py needs to import pinecone to function in this file
    # def store_item_doc_in_pinecone(index_name, item_doc):
    # try:
    #     # Initialize Pinecone index
    #     index = pinecone.Index(index_name)
    #     print("Initialized Pinecone index.")

    #     # Extract the unique ID of the item_doc
    #     item_doc_id = item_doc.id
    #     print(f"Extracted item_doc ID: {item_doc_id}")

    #     # Debug: print the attributes and their types
    #     print(f"Item_doc attributes and types: {[(attr, type(val)) for attr, val in item_doc.__dict__.items()]}")

    #     # Create an empty list to store vectors
    #     vector_dicts = []

    #     # Loop through each attribute in item_doc
    #     for attribute, value in item_doc.__dict__.items():
    #         # Check if the value is an embedding (ndarray or list)
    #         if isinstance(value, (ndarray, list)):
    #             # Create a unique ID for each attribute
    #             unique_id = f"{item_doc_id}_{attribute.replace('_embedding', '')}"
    #             print(f"Generated unique ID for attribute '{attribute}': {unique_id}")

    #             # If the value is an ndarray, convert it to list; otherwise, leave it as is
    #             vector_list = value.tolist() if isinstance(value, ndarray) else value
    #             print(f"Prepared list for attribute '{attribute}'.")

    #             # Append to list of vectors to be inserted
    #             vector_dicts.append({'id': unique_id, 'values': vector_list})
    #             print(f"Appended vector for attribute '{attribute}' to list of vectors to be inserted.")
        
    #     # Debug: print the vector_dicts before upsert
    #     print(f"Vector dicts to upsert: {vector_dicts}")

    #     # Insert vectors into Pinecone index
    #     index.upsert(vector_dicts)
    #     print(f"Vectors stored successfully in index '{index_name}' with IDs: {[d['id'] for d in vector_dicts]}")
        
    # except Exception as e:
    #     print(f"Error storing item_doc in index '{index_name}':", e)
