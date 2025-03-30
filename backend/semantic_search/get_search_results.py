import sqlite3
import pickle
import numpy as np
import openai
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import os

def get_embedding(text):
    response = openai.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding

def load_embeddings_from_pickle(EMBEDDINGS_PATH):
    with open(EMBEDDINGS_PATH, "rb") as f:
        embeddings = pickle.load(f)
    return embeddings

def semantic_search_results(query_text, top_n=5):  # Default to top 5
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
    DB_PATH = os.path.join(parent_dir, 'mental_health_data.db')
    EMBEDDINGS_PATH = os.path.join(parent_dir, 'embeddings_with_entry_numbers.pkl')


    prompt = f"""
                Your goal is to take the user's search query and fix any spelling mistakes in it. 
                Only output the fixed query, as the output will directly be fed into a search engine. 
                Only focus on fixing spelling mistakes, and changing wording only if it doens't make sense. 
                DO NOT change the context. Here is the search query: {query_text}
            """

    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(model="gpt-4o",  # or "gpt-4" if you want
        messages=[{"role": "system", "content": "You are a smart search engine."},
                    {"role": "user", "content": prompt}])
        query_text = response.choices[0].message.content.strip()
    except Exception as e:
        pass

    query_embedding = np.array(get_embedding(query_text)).reshape(1, -1)
    embeddings = load_embeddings_from_pickle(EMBEDDINGS_PATH)
    embeddings_np = np.array([embedding for entry_number, embedding in embeddings])

    if embeddings_np.shape[1] != query_embedding.shape[1]:
        raise ValueError(f"Embedding dimensionality mismatch")

    similarities = cosine_similarity(query_embedding, embeddings_np)[0]

    top_n_indices = similarities.argsort()[-top_n * 2:][::-1]  # Fetch more than top_n results to avoid duplicates
    SIMILARITY_THRESHOLD = 0.7
    filtered_indices = [idx for idx in top_n_indices if similarities[idx] >= SIMILARITY_THRESHOLD]  # Apply threshold


    top_results = []
    seen_pairs = set()  # To track already seen patient-counselor pairs
    idx = 0  # Start at the first result

    while len(top_results) < top_n and idx < len(filtered_indices):
        entry_number = embeddings[filtered_indices[idx]][0]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT patient_dialogue, counselor_dialogue, summary FROM dialogues WHERE entry_number = ?", (entry_number,))
        patient_dialogue, counselor_dialogue, summary = cursor.fetchone()
        conn.close()

        pair = (patient_dialogue, counselor_dialogue)

        # Check if the pair has been seen before, if so, skip
        if pair not in seen_pairs and patient_dialogue not None and patient_dialogue != "" and counselor_dialogue not None and counselor_dialogue != "":
            seen_pairs.add(pair)  # Add the current pair to the seen set
            top_results.append({
                "summary": summary,  # Replace with actual summary or logic
                "patient_dialogue": patient_dialogue,
                "counselor_dialogue": counselor_dialogue,
            })

        idx += 1  # Move to the next result

    return top_results