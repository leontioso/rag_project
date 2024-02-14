from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from openai import AzureOpenAI
from . import rag_frame
from qdrant_client import QdrantClient
from . import utils
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def index(request):
     
    return render(request, "conversation/conversation.html")


@api_view(['GET','POST'])
def api_data(request):
    azure_client = AzureOpenAI(
        api_key=os.getenv('AZURE_API_KEY'),  
        api_version=os.getenv('API_VERSION'),
        azure_endpoint= os.getenv('AZURE_ENDPOINT')
        )
    
    db_client = QdrantClient('localhost', port=6333)
    rag = rag_frame.RAG(db_client=db_client, llm_client=azure_client, collection_name="User1")
    try:
        query = request.data.get('prompt', '')
        query_embedding = utils.generate_embedding(azure_client, 'embedding-ada', query)

        similar_texts = rag.retrieve_docs(query_embedding, top_k_docs=1)
        messages = [{"role": "system", "content": similar_text} for similar_text in similar_texts]
        messages.append({"role": "user", "content": query})
        response = rag.generate_response(messages=messages, model_name="gpt-4-turbo")
    except Exception as e:
        print(e)
        response = "Access from the browser"
    return Response({"response" :response})