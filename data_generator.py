from config import DATA_PATH, GITHUB_REPO, GITHUB_TOKEN
from utils.scrapper import crawl_github_repo

url_collection = []
for repo in GITHUB_REPO:
    print(f"Extracting from repository: {repo}")
    try:
        code_files_urls = crawl_github_repo(repo, False, GITHUB_TOKEN)
        url_collection.extend(code_files_urls)
    except Exception as e:
        print(f"Failed extracting from repository: {repo}")
with open(DATA_PATH, "w") as f:
    for item in url_collection:
        f.write(item + "\n")
