from config import DATA_PATH, GOOGLE_API_KEY, PROMPT_CONTENT
from langchain.schema.document import Document
from langchain.text_splitter import Language
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_vertexai import VertexAIEmbeddings
from utils.extract_code_from_urls import (
    extract_python_code_from_ipynb,
    extract_python_code_from_py,
)
from llm.reponse import generate_reponse

MODEL_NAME = "gemini-pro"
MAX_OUTPUT_TOKENS = 2048
TEMP = 0.5
EMBEDDING_QPM = 100
EMBEDDING_NUM_BATCH = 5
TOP_K_NUM = 3

verbose = False

code_llm = GoogleGenerativeAI(
    model=MODEL_NAME,
    max_output_tokens=MAX_OUTPUT_TOKENS,
    temperature=TEMP,
    google_api_key=GOOGLE_API_KEY,
    verbose=False,
)

assert DATA_PATH.exists(), "Please run data_generator.py first"

with open(DATA_PATH) as f:
    code_files_urls = f.read().splitlines()

code_strings = []
for i in range(0, len(code_files_urls)):
    if code_files_urls[i].endswith(".ipynb"):
        content = extract_python_code_from_ipynb(code_files_urls[i], "code")
        doc = Document(
            page_content=content, metadata={"url": code_files_urls[i], "file_index": i}
        )
        code_strings.append(doc)
    elif code_files_urls[i].endswith(".py"):
        content = extract_python_code_from_py(code_files_urls[i])
        doc = Document(
            page_content=content, metadata={"url": code_files_urls[i], "file_index": i}
        )
        code_strings.append(doc)

text_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
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


input_prompt = input("Task: ")

result = generate_reponse(
    llm=code_llm,
    prompt_content=PROMPT_CONTENT,
    retriever=retriever,
    user_prompt=input_prompt,
)
