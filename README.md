# rag_project
## Overview
This repository contains code and resources for deploying a chatbot powered by a Retrieval-Augmented Generation (RAG) model. RAG is an advanced architecture that leverages the strengths of retrievers and generative models for tasks such as question answering, summarization, and conversational agents.
## Components
Basic components of RAG architecture is a Retriever component which is responsible to fetch the most similar documents to user's query and the Large Language Model (LLM) which is the generative component responsible for the response to the user. 
### Retriever Component
The structure of the Retriever Component relies to a vector database which stores user's data efficiently in embeddings format. The embedings that were used in current project is 'text-embedding-ada-002' and the vector database is Qdrant database deployed in a docker container.
### LLM model
The LLM model chosen for the generative part of RAG framework is 'gpt-4' which is provided by Microsoft Azure. 
