from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") 

def calling_llm(vectorstore,question):
    llm = ChatOpenAI(model = "o3-mini")

    prompt = ChatPromptTemplate.from_messages(
        [
        """
        Answer the questions based on the provided context try to be funny while answering the questions
        try to make some examples from real world for explaining the concepts well and do not provide the entire context if only partial information from the context is requested.
        
        
        <context>
        {context}
        </context>
        """
        ]
    )

    document_chain = create_stuff_documents_chain(llm,prompt)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    retrival_chain = create_retrieval_chain(retriever,document_chain)
    response = retrival_chain.invoke({"input":question})
    return response["answer"]

