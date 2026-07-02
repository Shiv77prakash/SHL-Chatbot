import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer


# -------------------------------
# Load Embedding Model
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------------
# Load FAISS Index
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_PATH = os.path.join(BASE_DIR, "vectorstore", "index.faiss")
METADATA_PATH = os.path.join(BASE_DIR, "vectorstore", "metadata.pkl")

index = faiss.read_index(INDEX_PATH)

with open(METADATA_PATH, "rb") as f:
    metadata = pickle.load(f)


# -------------------------------
# Search Function
# -------------------------------
def search_assessments(query, top_k=5):

    # Convert query into embedding
    query_embedding = model.encode([query])

    # Search in FAISS
    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:

        if idx == -1:
            continue

        results.append(metadata[idx])

    return results


# -------------------------------
# Testing
# -------------------------------
if __name__ == "__main__":

    query = input("Enter Search Query: ")

    results = search_assessments(query)

    print("\nTop Matching Assessments\n")

    for i, item in enumerate(results, 1):

        print(f"{i}. {item['name']}")
        print(f"URL : {item['url']}")
        print(f"Keys : {item['keys']}")
        print("-" * 50)