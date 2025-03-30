from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import modal

image = modal.Image.debian_slim().pip_install_from_requirements("requirements.txt") \
    .add_local_file('dataset.csv', '/root/dataset.csv') \
    .add_local_file('embeddings_with_entry_numbers.pkl', '/root/embeddings_with_entry_numbers.pkl') \
    .add_local_file('embeddings.pkl', '/root/embeddings.pkl') \
    .add_local_file('mental_health_data.db', '/root/mental_health_data.db') \
    .add_local_file('semantic_search/get_search_results.py', '/root/semantic_search/get_search_results.py') \
    .add_local_file('rag/generate_advice.py', '/root/rag/generate_advice.py') \
    .add_local_file('rag/llm.py', '/root/rag/llm.py') \
    .add_local_file('rag/rag_model.py', '/root/rag/rag_model.py') \
    .add_local_file('anxiety_model/model.py', '/root/anxiety_model/model.py')

app = modal.App("flask-app", image=image)
flask_app = Flask(__name__)
CORS(flask_app)

@flask_app.route('/generate_advice', methods=['POST'])
def get_advice():
    from rag.generate_advice import advice 
    data = request.json
    user_input = data.get("text", "")
    generated_advice = advice(user_input)
    return jsonify({"advice": generated_advice})

@flask_app.route('/search_results', methods=['POST'])
def search():
    from semantic_search.get_search_results import semantic_search_results
    data = request.json
    query_text = data.get("text", "")
    results = semantic_search_results(query_text)
    return jsonify({"results": results})

@flask_app.route('/predict_response', methods=['POST'])
def get_prediction():
    from anxiety_model.model import predict_anxiety_level
    data = request.json
    patient_transcript = data.get("text", "")
    anxiety_level = predict_anxiety_level([patient_transcript])
    return jsonify({"anxiety_level": anxiety_level})

@flask_app.route('/', methods=['POST'])
def test():
    return jsonify({"message": "Starting server"})

@app.function(secrets=[modal.Secret.from_name("legacy")])
@modal.wsgi_app()
def api():
    return flask_app
