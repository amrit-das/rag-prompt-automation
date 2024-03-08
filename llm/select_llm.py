from langchain_google_genai import GoogleGenerativeAI
from config import GOOGLE_API_KEY


def get_llm_model(model_name, max_output_tokens, temperature):
    if model_name == "llama2":
        llm = "llama2"
        # ToDo
    elif model_name == "GPT-4":
        llm = "gpt4"
        # ToDo
    else:
        model_name = "gemini-pro"
        llm = GoogleGenerativeAI(
            model=model_name,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            google_api_key=GOOGLE_API_KEY,
            verbose=False,
        )
    return llm
