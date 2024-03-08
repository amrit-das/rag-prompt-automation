from langchain_google_vertexai import VertexAIEmbeddings
from utils.extract_code_from_urls import (
    extract_python_code_from_ipynb,
    extract_python_code_from_py,
)
from config import DATA_PATH
from langchain.schema.document import Document
from langchain.text_splitter import Language
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import streamlit as st

EMBEDDING_QPM = 100
EMBEDDING_NUM_BATCH = 5
TOP_K_NUM = 3


@st.cache_resource
def generate_code_strings(code_files_urls):
    code_strings = []
    for i in range(0, len(code_files_urls)):
        if code_files_urls[i].endswith(".ipynb"):
            content = extract_python_code_from_ipynb(code_files_urls[i], "code")
            doc = Document(
                page_content=content,
                metadata={"url": code_files_urls[i], "file_index": i},
            )
            code_strings.append(doc)
        elif code_files_urls[i].endswith(".py"):
            content = extract_python_code_from_py(code_files_urls[i])
            doc = Document(
                page_content=content,
                metadata={"url": code_files_urls[i], "file_index": i},
            )
            code_strings.append(doc)
    return code_strings


def get_retriever(code_strings):
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=1000, chunk_overlap=150
    )
    texts = text_splitter.split_documents(code_strings)

    embeddings = VertexAIEmbeddings(
        requests_per_minute=EMBEDDING_QPM,
        num_instances_per_batch=EMBEDDING_NUM_BATCH,
        model_name="textembedding-gecko@latest",
    )

    db = FAISS.from_documents(texts, embeddings)

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K_NUM},
    )
    return retriever
