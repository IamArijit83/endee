from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np
import json
import os
import torch

# =========================
# 🔹 DEVICE CONFIG (GPU/CPU)
# =========================
device = 0 if torch.cuda.is_available() else -1

# =========================
# 🔹 MODELS
# =========================
# Embedding model (fast + lightweight)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Text generation model (RAG)
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    device=device
)

# =========================
# 🔹 STORAGE FILE (simulating Endee DB)
# =========================
DATA_FILE = "endee_store.json"

# Load existing data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        store = json.load(f)
else:
    store = []

# =========================
# 🔹 ADD DOCUMENTS
# =========================
def add_documents(texts):
    global store

    embeddings = embed_model.encode(texts).tolist()

    for text, emb in zip(texts, embeddings):
        store.append({
            "text": text,
            "vector": emb
        })

    # Save to disk (persistent storage)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f)


# =========================
# 🔹 SEARCH (VECTOR SIMILARITY)
# =========================
def search(query, top_k=3):
    if len(store) == 0:
        return ["No data available. Please upload a document first."]

    query_embedding = embed_model.encode([query])[0]

    vectors = np.array([item["vector"] for item in store])
    texts = [item["text"] for item in store]

    scores = np.dot(vectors, query_embedding)
    top_indices = np.argsort(scores)[-top_k:][::-1]

    return [texts[i] for i in top_indices]


# =========================
# 🔹 GENERATE FINAL ANSWER (RAG)
# =========================
def generate_answer(query):
    contexts = search(query)

    combined_context = " ".join(contexts)

    prompt = f"""
Answer the question based on the context below.

Context:
{combined_context}

Question:
{query}

Answer:
"""

    result = generator(
        prompt,
        max_length=200,
        do_sample=False
    )

    return result[0]["generated_text"]