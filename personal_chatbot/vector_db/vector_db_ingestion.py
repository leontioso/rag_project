import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
from openai import AzureOpenAI
from pathlib import Path
from utils import generate_embedding
from openai import AzureOpenAI

# Retrieval of environmental variables
load_dotenv(override=True)
api_key = os.environ['AZURE_API_KEY']
azure_endpoint = os.environ['AZURE_ENDPOINT']
api_version = os.environ['API_VERSION']

# initialization of the clients
db_client = QdrantClient("localhost", port=6333)
azure_client = AzureOpenAI(api_key=api_key, azure_endpoint=azure_endpoint, api_version=api_version)

# Checking for existing database. Otherwise creation of user's database
try:
    db_client.create_collection(
        collection_name="User1",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )
except:
    print("User's db already exists")
    
# Retrieve of the text of user's data
list_text_files = [file for file in Path('./external_data').iterdir() if file.is_file() and file.suffix == '.txt']
text_for_embed = list()
for text_file in list_text_files:
    with open(text_file) as file:
        text = " ".join(file.readlines())
        text_for_embed.append(text)

# Retrieval of doc embeddings
embeddings = [generate_embedding(azure_client, 'embedding-model', text) for text in text_for_embed]

# Ingestion of embeddings and their respective text
db_client.upsert(
    collection_name='User1',
    wait=True,
    points=[PointStruct(id=idx+1, vector=pair[0], payload={'article': pair[1]}) 
                for idx, pair in enumerate(zip(embeddings, text_for_embed, strict=True))]
    )