def chunk_file(file_content: str, max_lines: int = 100) -> list:
    lines = file_content.splitlines()
    chunks = []
    
    for i in range(0, len(lines), max_lines):
        chunk = "\n".join(lines[i:i + max_lines])
        chunks.append(chunk)
    
    return chunks