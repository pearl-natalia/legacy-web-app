import re
import os
import string
import nltk
import pickle
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
        re_url = re.compile(r'https?://\S+|www\.\S+')
        return re_url.sub('', text)

    def remove_punc(text):
        exclude = string.punctuation
        return text.translate(str.maketrans('', '', exclude))
    
    def remove_stopwords(text):
        stopwrds = stopwords.words('english')
        words = word_tokenize(text)
        return ' '.join([word for word in words if word not in stopwrds])

    # Preprocess the new text
    new_text_processed = [remove_url(text) for text in new_text]  # Remove URLs
    new_text_processed = [remove_punc(text) for text in new_text_processed]  # Remove punctuation
    new_text_processed = [remove_stopwords(text) for text in new_text_processed]  # Remove stopwords
    new_text_processed = [text.lower() for text in new_text_processed]  # Convert to lowercase

    with open('tfidf_vectorizer.pkl', 'rb') as tfidf_file:
        tfidf_vectorizer = pickle.load(tfidf_file)

    new_text_tfidf = tfidf_vectorizer.transform(new_text_processed).toarray()

    # Load Naive Bayes model
    with open('naive_bayes_model.pkl', 'rb') as model_file:
        nb = pickle.load(model_file)

    # Load Random Forest model
    with open('random_forest_model.pkl', 'rb') as rf_file:
        rf = pickle.load(rf_file)

    # Predict using the trained models
    probabilities_nb = nb.predict_proba(new_text_tfidf)  # Using Naive Bayes model
    probabilities_rf = rf.predict_proba(new_text_tfidf)  # Using Random Forest model

    normalized_probability = (probabilities_nb[1] + probabilities_rf[1]) / 2.0
    if normalized_probability < 0.3:
        return "Not Anxious"
    elif 0.3 <= normalized_probability < 0.6:
        return "Midly Anxious"
    elif 0.6 <= normalized_probability < 0.8:
        return "Moderately Anxious"
    elif 0.8 <= normalized_probability <= 1.0:
        return "Very Anxious"