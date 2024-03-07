from config import DATA_PATH, GOOGLE_API_KEY, PROMPT_CONTENT, PROMPT_CONTENT_LLM
from llm.select_llm import get_llm_model

from llm.rag_retriever import get_retriever
from llm.reponse import generate_response_llm, generate_reponse_rag
import streamlit as st

MAX_OUTPUT_TOKENS = 2048

st.set_page_config(
    page_title="Automator",
    page_icon=":scroll:",
)

st.title("RAG Automation Code Generator")

with st.sidebar:
    st.title("Configuration")
    st.subheader("Models and parameters")
    model_name = st.sidebar.selectbox(
        "Choose a Llama2 model",
        ["Gemini", "LLama", "GPT-4", "Mistral"],
        key="Gemini",
    )
    temp = st.slider("Temperature", min_value=1, max_value=99) / 100
    retr = st.radio("Retrieval", ["LLM", "RAG"])

st.write(f"Using {model_name} Model")

code_llm = get_llm_model(
    model_name=model_name, max_output_tokens=MAX_OUTPUT_TOKENS, temperature=temp
)
input_prompt = st.text_input("Enter Prompt for automation")

if retr == "RAG":
    assert DATA_PATH.exists(), "Please run data_generator.py first"
    with open(DATA_PATH) as f:
        code_files_urls = f.read().splitlines()
    retriever = get_retriever(code_files_urls)
    submit = st.button("Submit")
else:
    submit = st.button("Submit")

if submit:
    result = generate_response_llm(
        llm=code_llm,
        prompt_content=PROMPT_CONTENT_LLM,
        user_prompt=input_prompt,
    )
    st.write(result)
