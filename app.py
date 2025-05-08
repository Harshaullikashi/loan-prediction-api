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
        if "Income" not in data or "Credit_Score" not in data or "Loan_Amount" not in data:
            return jsonify({"error": "Missing required fields: Income, Credit_Score, Loan_Amount"})

        # Convert input data into a list for prediction
        input_features = [[data["Income"], data["Credit_Score"], data["Loan_Amount"]]]
        
        prediction = model.predict(input_features)  # Use ML model
        
        return jsonify({"Loan_Approval": "✅ Approved" if prediction[0] else "❌ Not Approved"})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)  # Enable debugging for troubleshooting


