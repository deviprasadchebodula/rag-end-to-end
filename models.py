####################### Models ###########################

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")
GROQ_MODEL="openai/gpt-oss-20b"
EMBED_MODEL="sentence-transformers/all-MiniLM-L6-v2"
llm = ChatGroq(api_key=GROQ_API_KEY,
                       model=GROQ_MODEL,
                       temperature=0) 
embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)