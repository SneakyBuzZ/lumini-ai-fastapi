from urllib.parse import urlparse

def parse_repo_url(repo_url: str):
    parts = urlparse(repo_url).path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")
    owner, repo = parts[0], parts[1].replace(".git", "")
    return owner, repo