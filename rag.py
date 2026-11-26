import os
from dotenv import load_dotenv
load_dotenv()

from data_loader import DATA_LOADER
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec, VectorType
from langchain_core.output_parsers import StrOutputParser

from models import llm, embedding
from prompt import prompt

PINECONE_INDEX = "sentence-vector-index"

# Initialize Pinecone (same as vector_db.py)
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

indexes=[index['name'] for index in pc.list_indexes()]
if PINECONE_INDEX not in indexes:
    index_config = pc.create_index(
                       name=PINECONE_INDEX,
                       dimension=384,
                       spec=ServerlessSpec(cloud='aws',region='us-east-1'),
                       vector_type=VectorType.DENSE
                                )


def doc_out(outputs):
    s='\n\n'.join(out.page_content for out in outputs)
    return(s)


def ingest_pdf(pdf_path, namespace):
    """load -> split -> embed -> store in Pinecone (one namespace per uploaded PDF)"""
    obj = DATA_LOADER(pdf_path)
    documents = obj.pdf_load()

    splitter = RecursiveCharacterTextSplitter()
    docs = splitter.split_documents(documents)

    PineconeVectorStore.from_documents(
        documents=docs,
        embedding=embedding,
        index_name=PINECONE_INDEX,
        namespace=namespace
    )
    return len(docs)


def ask(question, namespace):
    """retrieve from that PDF's namespace -> prompt -> llm"""
    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX,
        embedding=embedding,
        namespace=namespace
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    chain = ({'context': retriever | doc_out,
              'question': lambda x: x}
             |
             prompt
             |
             llm
             |
             StrOutputParser())

    for attempt in range(3):
        answer = chain.invoke(question)
        if isinstance(answer, str) and answer.strip():
            return answer.strip()

    return "The AI service is temporarily unavailable. Please try again."
