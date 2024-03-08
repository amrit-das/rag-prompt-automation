# Context Aware Automation Code Generator - RAG - Gemini - Langchain

This webapp takes input of user Prompt to convert it into Automation Tasks
It uses a RAG Pipeline and Gemini Model as its context model to understand context and Retrieve code from database.

Built in `python-3.11`


## Usage

#### Setup
```bash
git clone git@github.com:amrit-das/rag-prompt-automation.git
cd rag-prompt-automation
touch .env
```
Edit `.env` with relevant LLM API Keys (OpenAI API, Gemini API)

#### Installation
```bash
pip install -r requirements.txt
```
#### Execution
```bash
streamlit run main.py
```

## Demo
[streamlit-main-2024-03-09-00-03-52.webm](https://github.com/amrit-das/rag-prompt-automation/assets/31342979/eff77d21-024d-4872-a386-13b786f13a64)



## Authors

- [@amrit-das](https://www.github.com/amrit-das)


## Acknowledgements

### Datasets
- [Code Search Net - Hugging Face](https://huggingface.co/datasets/code_search_net)
- [Github Crawled Python Projects](https://github.com/amrit-das/rag-prompt-automation/blob/a80a89af3a4da621484b4f3ec83ec5f327236594/config.py#L13) 

### Reference
 - [Langchain - Docs](https://python.langchain.com/docs/get_started/introduction)
 - [Langchain - Google](https://python.langchain.com/docs/integrations/chat/google_generative_ai)
 - [Streamlit](https://docs.streamlit.io/)
 - [Mervin Haystack AI RAG Pipeline](https://mer.vin/2024/01/haystack-ai-to-create-rag-pipeline/)
