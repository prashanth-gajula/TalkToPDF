from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") 

def create_vector_store(documents):
    """Create vector store from documents"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    texts = text_splitter.split_documents(documents)
    
    embeddings = OpenAIEmbeddings()
    
    vector_store = FAISS.from_documents(texts, embeddings)
    return vector_store