from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List

def create_faiss_index(texts:List[str], model_name="all-MiniLM-L6-v2"):
    """
    Create a FAISS vector store from the provided documents using HuggingFace embeddings.
    
    Args:
        texts (List[str]): List of text documents to be indexed.
        Example: ["Document 1 text", "Document 2 text"]
        model_name (str): Name of the HuggingFace model to use for embeddings.
        
    Returns:
        FAISS: A FAISS vector store containing the document embeddings.
    """
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    faiss_index = FAISS.from_texts(texts, embeddings)
    return faiss_index

def retrieve_relevant_docs(vectorstore, query: str, k: int = 5):
    """
    This function retrieves relevant documents from the FAISS vector store based on a query.

    Args:
        vectorstore (FAISS): The FAISS vector store containing indexed documents.
        query (str): The query string to search for.
        Example: "What are the symptoms of diabetes?"
        k (int): The number of top relevant documents to retrieve. Default is 5.
    
    Returns:
        List[Document]: A list of documents that are most relevant to the query.
    """
    docs = vectorstore.similarity_search(query, k=k)
    return docs