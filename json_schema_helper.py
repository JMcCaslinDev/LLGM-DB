import json
import jsonschema
from jsonschema import validate
from jsonschema import RefResolver
import os

# Global dictionary to hold schemas
schemas = {}

def load_schemas():
    """
    Load all JSON schemas from the 'schemas' directory into a global dictionary.
    """
    global schemas
    schema_files = os.listdir('schemas')
    for file in schema_files:
        with open(f'schemas/{file}', 'r') as f:
            schema = json.load(f)
        schemas[file.replace('.schema.json', '').replace('.json', '')] = schema
    print(f"Loaded schemas: {list(schemas.keys())}")


def validate_json(json_data, schema_name):
    """
    Validate a JSON object against a schema.

    Parameters:
    - json_data (dict): The JSON object to validate.
    - schema_name (str): The name of the schema to validate against.

    Returns:
    - tuple: (is_valid (bool), error (str or None))
    """
    try:
        schema = schemas[schema_name]
        base_path = os.path.abspath('schemas')
        resolver = RefResolver(f'file://{base_path}/', schema)
        validate(instance=json_data, schema=schema, resolver=resolver)
    except jsonschema.exceptions.ValidationError as err:
        return False, str(err)
    return True, None


def store_json_to_vectordb(json_data, schema_name, index_name):
    """
    Store a valid JSON object in vectordb.

    Parameters:
    - json_data (dict): The JSON object to store.
    - schema_name (str): The name of the schema the JSON object should adhere to.

    Returns:
    - str: A message indicating success or failure.
    """
    is_valid, error = validate_json(json_data, schema_name)
    if not is_valid:
        return f"Invalid JSON data: {error}"
    
    # TODO: Embed JSON data into a vector here, if needed.
    # embedded_vector = ...

    # TODO: Store the vector in vectordb.
    # store_vectors(index_name, ids, [embedded_vector])
    
    return "Stored successfully"


def retrieve_json_from_vectordb(id, schema_name, index_name):
    """
    Retrieve a JSON object from vectordb by its ID.

    Parameters:
    - id (str): The ID of the JSON object in vectordb.
    - schema_name (str): The name of the schema the JSON object adheres to.

    Returns:
    - dict: The JSON object retrieved.
    """
    # TODO: Retrieve the vector from vectordb.
    # vector = retrieve_vector(index_name, id)

    # TODO: Convert the vector back to JSON data, if needed.
    # json_data = ...
    
    #return json_data

def print_json(json_data):
    """
    Print JSON data in a readable format.

    Parameters:
    - json_data (dict): The JSON object to print.
    """
    print(json.dumps(json_data, indent=4))

if __name__ == "__main__":
    load_schemas()
    # Your Vectordb operations here
