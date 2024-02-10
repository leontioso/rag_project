def generate_embedding(client, model_name, input_text):
    '''
    This is a functions that retrieves doc embeddings using Azure OpenAI API. 
    Embeddings are defined by model_name
    '''
    embedding = client.embeddings.create(input=[input_text], model=model_name).data[0].embedding
    return embedding
    