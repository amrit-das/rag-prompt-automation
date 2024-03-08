import nbformat
import requests
from functools import lru_cache

# Extracts the python code from an .ipynb file from github


@lru_cache(maxsize=128)
def extract_python_code_from_ipynb(github_url, cell_type="code"):
    raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace(
        "/blob/", "/"
    )

    response = requests.get(raw_url)
    response.raise_for_status()  # Check for any request errors

    notebook_content = response.text

    notebook = nbformat.reads(notebook_content, as_version=nbformat.NO_CONVERT)

    python_code = None

    for cell in notebook.cells:
        if cell.cell_type == cell_type:
            if not python_code:
                python_code = cell.source
            else:
                python_code += "\n" + cell.source

    return python_code


# Extracts the python code from an .py file from github
@lru_cache(maxsize=128)
def extract_python_code_from_py(github_url):
    raw_url = github_url.replace("github.com", "raw.githubusercontent.com").replace(
        "/blob/", "/"
    )

    response = requests.get(raw_url)
    response.raise_for_status()  # Check for any request errors

    python_code = response.text

    return python_code
