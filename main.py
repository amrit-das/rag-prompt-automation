from config import (
    DATA_PATH,
    PROMPT_CONTENT_RAG,
    PROMPT_CONTENT_LLM,
    PROMPT_CONTENT,
)
import re
from llm.select_llm import get_llm_model

from llm.rag_retriever import get_retriever, generate_code_strings
from llm.reponse import generate_response_llm, generate_response_rag
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
        "Choose an LLM model",
        ["Gemini", "LLama", "GPT-4", "Mistral"],
        key="Gemini",
    )
    temp = st.slider("Temperature", min_value=0, max_value=100) / 100
    retr = st.radio("Retrieval", ["LLM", "RAG"])

st.write(f"Using {model_name} Model")

code_llm = get_llm_model(
    model_name=model_name, max_output_tokens=MAX_OUTPUT_TOKENS, temperature=temp
)
input_prompt = st.text_area("Enter Prompt for automation")

if retr == "RAG":
    assert DATA_PATH.exists(), "Please run data_generator.py first"
    with open(DATA_PATH) as f:
        code_files_urls = f.read().splitlines()

    code_strings = generate_code_strings(code_files_urls)
    with st.spinner(text="Runnning Retriever"):
        retriever = get_retriever(code_strings)
    submit = st.button("Submit RAG")
else:
    submit = st.button("Submit LLM")

result = []
if submit:
    with st.spinner(text="This may take a moment..."):

        result = generate_response_llm(
            llm=code_llm,
            prompt_content=PROMPT_CONTENT,
            user_prompt=input_prompt,
        )

    with st.expander("Automation Tasks"):
        st.write(result)

    pattern = r"\*\sSTEP\d+\:\s"
    tasks = [re.sub(pattern, "", step) for step in result.splitlines()]

    if "expanded_states" not in st.session_state:
        st.session_state["expanded_states"] = [False] * len(tasks)

    for idx, task in enumerate(tasks):
        with st.spinner(f"Generating Code for Step{idx+1}: "):
            with st.expander(f"Step{idx+1}: {task}"):
                if retr == "LLM":
                    code = generate_response_llm(
                        llm=code_llm,
                        prompt_content=PROMPT_CONTENT_LLM,
                        user_prompt=task,
                    )
                    st.write(code)
                else:
                    code = generate_response_rag(
                        llm=code_llm,
                        prompt_content=PROMPT_CONTENT_RAG,
                        retriever=retriever,
                        question=task,
                    )
                    st.write(code["result"], code["source_documents"])
