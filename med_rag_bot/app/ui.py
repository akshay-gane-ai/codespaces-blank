import streamlit as st

def pdf_uploader():
    """
    Streamlit component to upload a PDF file.
    
    Returns:
        str: The path to the uploaded PDF file.
    """
    return st.file_uploader("Upload a PDF file", type=["pdf"], accept_multiple_files=True, help="Upload one or more pdf file(s)")