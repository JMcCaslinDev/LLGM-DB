from typing import Any, Iterable
import numpy as np
from pydantic import BaseModel, Field, validator, root_validator

class VariableEmbeddingPair(BaseModel):
    variable: Any = Field(...)
    embedding: np.ndarray = Field(...)
    size: int = Field(None)

    @classmethod
    def __get_validators__(cls) -> Iterable:
        yield cls.validate

    @classmethod
    def validate(cls, value):
        return value  # Custom validation logic can be placed here

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(
            type='object',
            properties={
                'variable': {'type': 'string'},
                'size': {'type': 'integer'},
                'embedding': {'type': 'array', 'items': {'type': 'number'}}
            }
        )
        
    @validator('embedding', pre=True, always=True)
    def validate_embedding(cls, value, values):
        if value is None:
            raise ValueError("Embedding cannot be None.")
        size = values.get('size')
        if size is not None and value.shape[0] != size:
            raise ValueError(f"Embedding size must be {size}.")
        return value

    @root_validator(pre=True)
    def check_variable_and_embedding(cls, values):
        variable = values.get('variable')
        embedding = values.get('embedding')
        if variable is None or embedding is None:
            raise ValueError("Both a variable and an embedding must be provided.")
        return values

    class Config:
        arbitrary_types_allowed = True
