import re
import os
import string
import nltk
import pickle
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def predict_anxiety_level(new_text):
    nltk_data_dir = os.getcwd()  # Current working directory
    nltk.data.path.append(nltk_data_dir)

    if not os.path.exists(os.path.join(nltk_data_dir, 'tokenizers', 'punkt')):
        print("Downloading punkt...")
        nltk.download('punkt', download_dir=nltk_data_dir)

    if not os.path.exists(os.path.join(nltk_data_dir, 'corpora', 'stopwords')):
        print("Downloading stopwords...")
        nltk.download('stopwords', download_dir=nltk_data_dir)

    def remove_url(text):
        re_url = re.compile(r'https?://\S+|www\.\S+')  # Fixed invalid escape sequence
        return re_url.sub('', text)
    
    def remove_punc(text):
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def remove_stopwords(text):
        stopwrds = set(stopwords.words('english'))  # Use a set for faster lookup
        words = word_tokenize(text)
        return ' '.join([word for word in words if word.lower() not in stopwrds])  # Convert to lowercase before checking

    # Ensure new_text is a list
    if isinstance(new_text, str):
        new_text = [new_text]  # Convert to list

    # Apply preprocessing
    new_text_processed = [remove_url(text) for text in new_text]
    new_text_processed = [remove_punc(text) for text in new_text_processed]
    new_text_processed = [remove_stopwords(text) for text in new_text_processed]
    new_text_processed = [text.lower() for text in new_text_processed]

    # Load the trained TF-IDF vectorizer
    with open('tfidf_vectorizer.pkl', 'rb') as tfidf_file:
        tfidf = pickle.load(tfidf_file)
    
    # Transform new text
    new_text_tfidf = tfidf.transform(new_text_processed).toarray()

    # Load models
    with open('naive_bayes_model.pkl', 'rb') as model_file:
        nb = pickle.load(model_file)

    with open('random_forest_model.pkl', 'rb') as rf_file:
        rf = pickle.load(rf_file)

    # Predict probabilities
    probabilities_nb = nb.predict_proba(new_text_tfidf)
    probabilities_rf = rf.predict_proba(new_text_tfidf)

    print(f"Naive Bayes Probabilities: {probabilities_nb}")
    print(f"Random Forest Probabilities: {probabilities_rf}")

    # Extract anxiety probability (index 1 is the probability of being "Anxious")
    probability_nb = probabilities_nb[0][1]
    probability_rf = probabilities_rf[0][1]
    print(f"Naive Bayes Anxiety Probability: {probability_nb}")
    print(f"Random Forest Anxiety Probability: {probability_rf}")

    # Normalize the probability
    normalized_probability = (probability_nb + probability_rf) / 2.0
    print(f"Normalized Probability: {normalized_probability}")

    # Return the appropriate anxiety level
    if normalized_probability < 0.3:
        return "Not Anxious"
    elif 0.3 <= normalized_probability < 0.6:
        return "Mildly Anxious"
    elif 0.6 <= normalized_probability < 0.8:
        return "Moderately Anxious"
    else:
        return "Very Anxious"

if __name__ == "__main__":
    result = predict_anxiety_level("I'm super relaxed.")
    print(f"Predicted Anxiety Level: {result}")
