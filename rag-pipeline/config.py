import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DATA_PATH = Path("knowledge") / "code_files_urls.txt"

GITHUB_REPO = [
    "prathimacode-hub/Awesome_Python_Scripts",
    "adnanh/webhook",
    "chaoss/grimoirelab-perceval",
    "Logan1x/Python-Scripts",
    "larymak/Python-project-Scripts",
]

PROMPT_CONTENT = """
    Role: You are a proficient python developer, specializing in Automation Tasks.
    Task: Respond with the syntactically correct code for to the automation task below. Make sure you follow rules below:
    Rules:
    1. Use context to understand the task and how to perform it in python.
    2. Do not add license information to the output code.
    3. Ensure all the requirements in the question are met.
    4. Make sure to write complete scripts not just outlines.

    Task:
    {question}

    Context:
    {context}

    Helpful Response :
    """
