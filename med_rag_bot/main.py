from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.chat_utils import get_chat_model, ask_chat_model
from app.pdf_utils import extract_text_from_pdf
from app.vectorstore_utils import create_faiss_index, retrieve_relevant_docs
from app.ui import pdf_uploader
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="med_rag_bot/app/.env")

EURI_API_KEY = os.getenv("EURI_API_KEY")

# Set page config with title and icon
st.set_page_config(
    page_title="MedRAG Chatbot",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_model" not in st.session_state:
    st.session_state.chat_model = None

# Sidebar configuration
with st.sidebar:
    st.title("MedRAG Bot")
    st.markdown("Welcome to your medical document assistant!")
    st.markdown("---")
    st.write("Upload PDFs, configure settings, and start chatting.")

    upload_files = pdf_uploader()   
    if upload_files:
        st.success("{} PDFs uploaded and indexed successfully!".format(len(upload_files)))

        if st.button("Process PDFs", type="primary"):
            with st.spinner("Processing PDFs..."):
                text_data = []
                for file in upload_files:
                    text = extract_text_from_pdf(file)
                    text_data.append(text)

                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len )
                chunks = []
                for text in text_data:
                    chunks.extend(text_splitter.split_text(text))  

                vectorstore = create_faiss_index(chunks)
                st.session_state.vectorstore = vectorstore

                chat_model = get_chat_model()
                st.session_state.chat_model = chat_model

                st.success("PDFs processed and indexed successfully!")
                st.balloons("Ready to chat with your documents!")

# Main page layout
st.header("MedRAG Chatbot 🩺")
st.write("Ask questions about your uploaded medical documents.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

if prompt := st.chat_input("Ask a question about your medical documents..."):
    if not st.session_state.vectorstore:
        st.error("Please upload and process PDFs first!")
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "timestamp": st.time()
            })

        with st.spinner("Retrieving relevant documents..."):
            relevant_docs = retrieve_relevant_docs(st.session_state.vectorstore, prompt)

        if relevant_docs:
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            system_prompt = f""" You are a medical assistant chatbot. Use the following context to answer the user's question. 
            You must always provide a response based on the context provided 
            and if do not know the answer, say "I don't know" 
            rather than making up an answer.
            
            Medical Documents:{context}
            
            User Question: {prompt}

            Answer: """

            with st.spinner("Generating response..."):
                response = ask_chat_model(st.session_state.chat_model, system_prompt)

            with st.chat_message("assistant"):
                st.markdown(response)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": st.time()
                })
        else:
            with st.chat_message("assistant"):
                response = "No relevant documents found. Please try asking something else."
                st.markdown(response)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": st.time()
                })

