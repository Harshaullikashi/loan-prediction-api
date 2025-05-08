from flask import Flask, request, jsonify
import pickle

# Initialize Flask App
app = Flask(__name__)  

# Load ML Model
try:
    model = pickle.load(open("loan_model.pkl", "rb"))  # Ensure the model file exists
except FileNotFoundError:
    model = None  # Handle missing model gracefully

@app.route('/')
def home():
    return "🏦 Loan Approval API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model file not found. Make sure 'loan_model.pkl' exists."})

    try:
        data = request.json  # Extract JSON input

        # Validate incoming JSON
        if not all(key in data for key in ["Income", "Credit_Score", "Loan_Amount"]):
            return jsonify({"error": "Missing required fields: Income, Credit_Score, Loan_Amount"})

        # Convert input data into a list for prediction
        input_features = [[data["Income"],
