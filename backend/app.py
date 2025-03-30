from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from rag.generate_advice import advice 
from semantic_search.get_search_results import semantic_search_results
app = Flask(__name__)
CORS(app)

@app.route('/generate_advice', methods=['POST'])
def get_advice():
    data = request.json
    user_input = data.get("text", "")
    generated_advice = advice(user_input)
    return jsonify({"advice": generated_advice})

@app.route('/search_results', methods=['POST'])
def search():
    data = request.json
    query_text = data.get("text", "")
    results = semantic_search_results(query_text)
    return jsonify({"results": results})

@app.route('/predict_response', methods=['POST'])
def get_prediction():
    return jsonify({"message": "Prediction completed!"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
