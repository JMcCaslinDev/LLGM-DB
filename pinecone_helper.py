import pinecone
from numpy import ndarray
from config import PINECONE_API_KEY


#   Initilize pinecone with the api key
def initialize_pinecone(): #   works
    try:
        pinecone.init(api_key=PINECONE_API_KEY, environment="us-west1-gcp-free")
        print("Pinecone initialized successfully")
    except Exception as e:
        print("Error initializing Pinecone:", e)


#   Create / Join the specified index, aka the vector database
def ensure_index_exists(index_name, dimension=1536): #   works
    try:
        if index_name in pinecone.list_indexes():
            print(f"Index '{index_name}' already exists. Connecting to it.")
        else:
            # Create the index with the specified dimension
            pinecone.create_index(index_name, dimension=dimension, metric="cosine")
            print(f"Index '{index_name}' created successfully")
    except Exception as e:
        print(f"Error creating or connecting to index '{index_name}':", e)





#   Store 1 or more vectors by passing the ids and vector data 
def store_vectors(index_name, ids, vectors): #   works for 1 vector at a time tested unsure about multiple
    try:
        index = pinecone.Index(index_name)
        # Convert vectors to a list of dictionaries with 'id' and 'values' keys
        vector_dicts = [{'id': id, 'values': vector} for id, vector in zip(ids, vectors)]
        index.upsert(vector_dicts)
        print(f"Vectors stored successfully in index '{index_name}'")
    except Exception as e:
        print(f"Error storing vectors in index '{index_name}':", e)


#   Deletes vectors based on a list of ids of vectors
def delete_vectors(index_name, ids): #   works
    try:
        index = pinecone.Index(index_name)
        index.delete(ids)
        print("\nDeleting ids: ", ids, "\n")

        print(f"Vectors deleted successfully from index '{index_name}'")
    except Exception as e:
        print(f"Error deleting vectors from index '{index_name}':", e)


#   untested if working     this doesnt rlly update it deletes then stores a new one idk if its intended this way
def update_vector(index_name, id, new_vector):
    try:
        delete_vectors(index_name, [id])
        store_vectors(index_name, [id], [new_vector])
        print(f"Vector updated successfully in index '{index_name}'")
    except Exception as e:
        print(f"Error updating vector in index '{index_name}':", e)


#   Search the vectordb for a similiar match to the embedded string you want to look up
def query_index(index_name, query_vector, top_k=10): #   works
    try:
        index = pinecone.Index(index_name)
        results = index.query(queries=[query_vector], top_k=top_k)
        print("Complete query results:")
        print(results)

        if results and 'results' in results and len(results['results']) > 0 and 'matches' in results['results'][0]:
            matches = results['results'][0]['matches']
            print("Query results:")
            for result in matches:
                print(result['id'], result['score'])
        else:
            print("No query results found.")
    except Exception as e:
        print(f"Error querying index '{index_name}':", e)



#   doesnt work currently
def get_all_vectors(index_name, batch_size=1000):
    print("entered get_all_vectors")
    try:
        index = pinecone.Index(index_name)
        print("index: ", index)
        if index.info().dimension == 0:     #this line breaks this index.info not recongized. idk why
            # The index is empty, return None
            print("returning")
            return None

        all_vectors = {}
        offset = 0
        print("first")
        while True:
            print("first-andhalf")
            # Query with an empty list of IDs and a batch_size limit
            results = index.query(queries=[[]], top_k=batch_size, offset=offset)
            print("second")
            if results and 'results' in results and len(results['results']) > 0 and 'matches' in results['results'][0]:
                matches = results['results'][0]['matches']
                for result in matches:
                    all_vectors[result['id']] = result['values']
                offset += batch_size
            else:
                break
        return all_vectors
    except Exception as e:
        raise e




def store_item_doc_in_pinecone(index_name, item_doc):
    try:
        # Initialize Pinecone index
        index = pinecone.Index(index_name)
        print("Initialized Pinecone index.")

        # Extract the unique ID of the item_doc
        item_doc_id = item_doc.id
        print(f"Extracted item_doc ID: {item_doc_id}")

        # Debug: print the attributes and their types
        print(f"Item_doc attributes and types: {[(attr, type(val)) for attr, val in item_doc.__dict__.items()]}")

        # Create an empty list to store vectors
        vector_dicts = []

        # Loop through each attribute in item_doc
        for attribute, value in item_doc.__dict__.items():
            # Check if the value is an embedding (ndarray or list)
            if isinstance(value, (ndarray, list)):
                # Create a unique ID for each attribute
                unique_id = f"{item_doc_id}_{attribute.replace('_embedding', '')}"
                print(f"Generated unique ID for attribute '{attribute}': {unique_id}")

                # If the value is an ndarray, convert it to list; otherwise, leave it as is
                vector_list = value.tolist() if isinstance(value, ndarray) else value
                print(f"Prepared list for attribute '{attribute}'.")

                # Append to list of vectors to be inserted
                vector_dicts.append({'id': unique_id, 'values': vector_list})
                print(f"Appended vector for attribute '{attribute}' to list of vectors to be inserted.")
        
        # Debug: print the vector_dicts before upsert
        print(f"Vector dicts to upsert: {vector_dicts}")

        # Insert vectors into Pinecone index
        index.upsert(vector_dicts)
        print(f"Vectors stored successfully in index '{index_name}' with IDs: {[d['id'] for d in vector_dicts]}")
        
    except Exception as e:
        print(f"Error storing item_doc in index '{index_name}':", e)


#TODO: Add a function that will take in a json data and store it in the vectordb may need embeddings made for it
#unsure of how this will work need to look at sample jsson data schema in other github repo to know what to have this handle
#   May also need to have a function that can query by json object delete by json object and update vector given a json object unsure yet if string case will handle this or if new functions for this spcifically will be needed




# TODO: Add a function to batch insert vectors for efficiency
# def batch_insert_vectors(index_name, ids, vectors):
#     pass

# TODO: Add a function to fetch a specific vector by its ID
# def fetch_vector_by_id(index_name, vector_id):
#     pass

# TODO: Add a function to fetch vectors by a list of IDs
# def fetch_vectors_by_ids(index_name, vector_ids):
#     pass



# TODO: Add a function to update vectors in a batch
# def batch_update_vectors(index_name, ids, vectors):
#     pass



# TODO: Add a function to compute similarity between two vectors in the index
# def compute_similarity(index_name, id1, id2):
#     pass

# TODO: Add a function to clear all vectors from the index
# def clear_all_vectors(index_name):
#     pass



# TODO: Add a function to export all vectors to a file
# def export_vectors_to_file(index_name, file_path):
#     pass

# TODO: Add a function to import vectors from a file
# def import_vectors_from_file(index_name, file_path):
#     pass


# TODO: Add a function to perform advanced query logic
# def advanced_query(index_name, query_vector, filters, top_k=10):
#     pass