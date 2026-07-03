import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

# -------------------------------
# Paths
# -------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_PATH = os.path.join(BASE_DIR, "vectorstore", "index.faiss")
METADATA_PATH = os.path.join(BASE_DIR, "vectorstore", "metadata.pkl")

# -------------------------------
# Lazy Loaded Objects
# -------------------------------

model = None
index = None
metadata = None


def load_resources():
    global model, index, metadata

    if model is None:
        print("Loading SentenceTransformer...")
        model = SentenceTransformer("all-MiniLM-L6-v2")

    if index is None:
        print("Loading FAISS Index...")
        index = faiss.read_index(INDEX_PATH)

    if metadata is None:
        print("Loading Metadata...")
        with open(METADATA_PATH, "rb") as f:
            metadata = pickle.load(f)


# -------------------------------
# Search
# -------------------------------

def search_assessments(query, top_k=5):

    load_resources()

    query_embedding = model.encode([query])

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

    while True:

        query = input("Query : ")

        results = search_assessments(query)

        print()

        for item in results:

            print(item["name"])
