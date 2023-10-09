import pinecone
from config import PINECONE_API_KEY


def initialize_pinecone():
    try:
        pinecone.init(api_key=PINECONE_API_KEY, environment="us-west1-gcp-free")
        print("Pinecone initialized successfully")
    except Exception as e:
        print("Error initializing Pinecone:", e)


def ensure_index_exists(index_name, dimension=1536):
    try:
        if index_name in pinecone.list_indexes():
            print(f"Index '{index_name}' already exists. Connecting to it.")
        else:
            # Create the index with the specified dimension
            pinecone.create_index(index_name, dimension=dimension, metric="cosine")
            print(f"Index '{index_name}' created successfully")
    except Exception as e:
        print(f"Error creating or connecting to index '{index_name}':", e)



def store_vectors(index_name, ids, vectors):
    try:
        index = pinecone.Index(index_name)
        # Convert vectors to a list of dictionaries with 'id' and 'values' keys
        vector_dicts = [{'id': id, 'values': vector} for id, vector in zip(ids, vectors)]
        index.upsert(vector_dicts)
        print(f"Vectors stored successfully in index '{index_name}'")
    except Exception as e:
        print(f"Error storing vectors in index '{index_name}':", e)


def delete_vectors(index_name, ids):
    try:
        index = pinecone.Index(index_name)
        index.delete(ids)
        print(f"Vectors deleted successfully from index '{index_name}'")
    except Exception as e:
        print(f"Error deleting vectors from index '{index_name}':", e)


def update_vector(index_name, id, new_vector):
    try:
        delete_vectors(index_name, [id])
        store_vectors(index_name, [id], [new_vector])
        print(f"Vector updated successfully in index '{index_name}'")
    except Exception as e:
        print(f"Error updating vector in index '{index_name}':", e)



def query_index(index_name, query_vector, top_k=10):
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
