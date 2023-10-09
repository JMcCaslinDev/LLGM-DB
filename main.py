import logging
logging.basicConfig(level=logging.INFO)

import pinecone_helper
import openai_helper

if __name__ == "__main__":
    try:
        logging.info("Initializing Pinecone.")
        pinecone_helper.initialize_pinecone()

        index_name = "llgm"
        dimension = 1536  # Update this to match the dimension of your embeddings

        logging.info(f"\nInitializing index '{index_name}'...")
        pinecone_helper.ensure_index_exists(index_name, dimension=dimension)

        sentence = "eastridge village by the waterfall"
        word = "eastridge village"

        logging.info(f"\nGenerating embedding for sentence: {sentence}")
        embedded_sentence = openai_helper.generate_embedding(sentence)
        logging.info(f"\nGenerating embedding for word: {word}")
        embedded_word = openai_helper.generate_embedding(word)

        # After generating embeddings
        if embedded_sentence is not None and embedded_word is not None:
            logging.info(f"\nSuccessfully generated embeddings.")
            logging.info(f"Type of embedded_sentence: {type(embedded_sentence)}, first few elements: {embedded_sentence[:10]}")
            logging.info(f"Type of embedded_word: {type(embedded_word)}, first few elements: {embedded_word[:10]}")

            #   Store a description of eastridge village in the vectordb
            print("\n\n")
            logging.info(f"\nStoring embeddings in vector database...")
            ids = ["eastridge_village_by_the_waterfall_id"]
            vectors = [embedded_sentence]
            pinecone_helper.store_vectors(index_name, ids, vectors)

            #   Query the database for the words eastridge village
            print("\n\n")
            logging.info(f"\nQuerying database for: {word}...")
            pinecone_helper.query_index(index_name, embedded_word, top_k=5)

            #   Test the delete function on eastridge village description
            print("\n\n")
            # Test the delete_vectors function
            delete_ids = ["eastridge_village_by_the_waterfall_id"]
            pinecone_helper.delete_vectors(index_name, delete_ids)
            logging.info(f"\nDeleted vectors with IDs: {delete_ids}")


            # #   Test the update_vector function
            # print("\n\n")
            # update_id = "eastridge_village_id"
            # new_vector = [0.1] * dimension  # Replace with the new vector you want to use
            # pinecone_helper.update_vector(index_name, update_id, new_vector)
            # logging.info(f"\nUpdated vector with ID: {update_id}")


            #   Query Database again for the word after the delete function has been run.
            print("\n\n")
            logging.info(f"\nQuerying database for: {word}...")
            pinecone_helper.query_index(index_name, embedded_word, top_k=5)

            # print("\n\n")
            # # Display the entire vector database if it's not empty
            # all_vectors = pinecone_helper.get_all_vectors(index_name)
            # if all_vectors is not None:
            #     logging.info("\nDisplaying the entire vector database:")
            #     for id, vector in all_vectors.items():
            #         logging.info(f"ID: {id}, Vector: {vector[:10]}")
            # else:
            #     logging.error("Failed to retrieve vectors from the database.")


        else:
            logging.error("One or both embeddings failed to generate.")
            exit(1)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        exit(1)
