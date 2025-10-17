from sentence_transformers import SentenceTransformer
from app._core.responses import AppError

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> list[float]:
    embedding = model.encode(text)
    return embedding.tolist()

def generate_file_embeddings(file_summary : str) -> list[float]:
    return generate_embedding(file_summary)

def generate_files_embeddings(files : list[dict], lab_id : str) -> list[dict]:
    if not lab_id:
        raise AppError(400, "lab_id is required to generate embeddings.")
    for file in files:
        file['embedding'] = generate_file_embeddings(file['summary'])
    summary_embeddings = [
        {
            "id" : idx,
            "vector" : file['embedding'],
            "payload" : {
                "lab_id": lab_id,
                "file_id" : file['id'],
                "file_name" : file['name'],
            }
        }
        for idx, file in enumerate(files)
    ]
    return summary_embeddings