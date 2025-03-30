import os
import pandas as pd
from dotenv import load_dotenv
import numpy as np
import openai
import pickle
from sklearn.metrics.pairwise import cosine_similarity

def get_embedding(text):
    response = openai.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding

def get_RAG_content(input_text):
    # Load data
    load_dotenv()
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))  
    dataset_file = os.path.join(parent_dir, 'dataset.csv')
    DATASET_PATH =os.path.join(parent_dir, 'dataset.csv')
    EMBEDDINGS_PATH = os.path.join(parent_dir, 'embeddings.pkl')
    df = pd.read_csv(DATASET_PATH)
    df.columns = ["context", "response"]

    # Embedd text
    if os.path.exists(EMBEDDINGS_PATH):
        with open(EMBEDDINGS_PATH, "rb") as f:
            dataset_embeddings = pickle.load(f)
    # Comment back in later
    # else:
    #     dataset_embeddings = [get_embedding(text) for text in df["context"]]
    #     with open(EMBEDDINGS_PATH, "wb") as f:
    #         pickle.dump(dataset_embeddings, f)

    input_embedding = np.array(get_embedding(input_text)).reshape(1, -1)
    dataset_embeddings_np = np.array(dataset_embeddings)

    # cosSim
    similarities = cosine_similarity(input_embedding, dataset_embeddings_np)[0]
    most_similar_idx = np.argmax(similarities)
    return df.iloc[most_similar_idx]["context"], df.iloc[most_similar_idx]["response"]
