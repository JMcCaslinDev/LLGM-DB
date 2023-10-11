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