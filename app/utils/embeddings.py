import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load assessments
with open("data/assessments.json", "r") as file:
    assessments = json.load(file)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create text list
texts = []

for assessment in assessments:

    combined_text = (
    assessment["name"] + " " +
    assessment["description"] + " " +
    assessment.get("test_type", "") + " " +
    "software developer backend developer api database programming dotnet ado.net sql"
)
    texts.append(combined_text)

# Generate embeddings
embeddings = model.encode(texts)

# Convert to numpy array
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# Save FAISS index
faiss.write_index(index, "data/faiss_index.index")

print("Embeddings generated successfully")