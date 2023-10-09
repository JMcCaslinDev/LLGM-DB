# LLGM DB

## Overview

This GitHub repository hosts the VectorDB component of my capstone project, which involves building an AI Gamemaster. The aim of this project is to create an intelligent game master capable of understanding context within a game. The VectorDB, powered by Pinecone and OpenAI, plays a crucial role in storing and retrieving the data necessary for the AI Gamemaster's operation.

## Features

-   generate_embedding(working) create embeddings using openai api from a string sentence returns the embeddings as a list of vectors
-   ensure_index_exists(working) check if the index exists so it connects instead of trying to create one 
-   store_vectors(working) store a string and embedding into the VectorDB
-   delete_vectors(working) Delete a vector entry in the database based on id
-   update_vector(unsure) Update a certain vector based on id
-   query_index(working) Get information from the database based on a string sentence
-   get_all_vectors(not working) Retreieve entire vectordb to print out and see

## Getting Started

Install everything in the requirments file and run the main.py file

## Installation



## Usage

Show examples of how to use your project.

## Contributing

Explain how others can contribute to your project.

## License

Specify the project's license.

## Acknowledgments

Mention any acknowledgments or credits.

## Notes

Add notes, known issues, or anything else relevant.
