class RAG():
    '''
    This is a class for the retrieve procedure of similar docs
    '''
    
    def __init__(self, *, db_client, llm_client, collection_name):
        '''
        Initialization of of a retrieval instance that aims to
        fetch the top_k docs which are more similar to user's query
        '''
        self.collection_name = collection_name
        self.client = db_client
        self.llm_client = llm_client
        
    def retrieve_docs(self, query_vector, *, top_k_docs):
        '''
        A method that performs the retrieval action from a
        Qdrant vector database
        '''
        search_results = self.client.search(collection_name=self.collection_name,
                                            query_vector=query_vector,
                                            limit=top_k_docs)
        list_results = [result.payload['article'] for result in search_results]
        return list_results
    
    def generate_response(self, *, model_name, messages):
        '''
        Method that sends similar docs and user's query to LLM 
        and returns the response
        '''
        response = self.llm_client.chat.completions.create(
        model=model_name, 
        messages=messages)
        return response.choices[0].message.content
        
        
        