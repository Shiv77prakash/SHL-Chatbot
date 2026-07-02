import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read catalog
with open("../data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = []
metadata = []

for item in catalog:

    text = f"""
    Name: {item.get("name","")}

    Description: {item.get("description","")}

    Job Levels: {", ".join(item.get("job_levels",[]))}

    Keys: {", ".join(item.get("keys",[]))}

    Languages: {", ".join(item.get("languages",[]))}

    Remote: {item.get("remote","")}

    Adaptive: {item.get("adaptive","")}
    """

    texts.append(text)

    metadata.append({
        "name": item.get("name"),
        "url": item.get("link"),
        "description": item.get("description"),
        "keys": item.get("keys"),
        "job_levels": item.get("job_levels"),
        "languages": item.get("languages")
    })

print("Creating Embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, "index.faiss")

with open("metadata.pkl","wb") as f:
    pickle.dump(metadata,f)

print("Done!")

print("Total Assessments :",len(metadata))