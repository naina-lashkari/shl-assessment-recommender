import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load assessments
with open("data/assessments.json", "r") as file:
    assessments = json.load(file)

# Load FAISS index
index = faiss.read_index("data/faiss_index.index")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def search_assessments(query, top_k=3):

    # Convert query into embedding
    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    # Search FAISS index
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:

        results.append(assessments[idx])

    return results