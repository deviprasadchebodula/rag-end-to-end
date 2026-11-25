############## Vector DB code ############

from splitter import docs
from models import embedding

import os
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from pinecone import ServerlessSpec,VectorType

# Set the environment variable
from dotenv import load_dotenv
load_dotenv()

PINECONE_INDEX = "sentence-vector-index"

# Initialize Pinecone
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])


indexes=[index['name'] for index in pc.list_indexes()]
if PINECONE_INDEX not in indexes:
    index_config = pc.create_index(
                       name=PINECONE_INDEX,
                       dimension=384,
                       spec=ServerlessSpec(cloud='aws',region='us-east-1'),
                       vector_type=VectorType.DENSE
                                )

# Now create the vector store
vector_store = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=embedding,
    index_name=PINECONE_INDEX
)