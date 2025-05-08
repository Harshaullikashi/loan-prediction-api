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
        # ✅ Get JSON input before using 'data'
        data = request.json  

        # ✅ Validate input fields
        required_fields = ["Income", "Credit_Score", "Loan_Amount"]
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"})

        # ✅ Use 'data' after defining it
        input_features = [[data["Income"], data["Credit_Score"], data["Loan_Amount"]]]
        
        prediction = model.predict(input_features)  # Use ML model
        
        return jsonify({"Loan_Approval": "✅ Approved" if prediction[0] else "❌ Not Approved"})
    
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Ensure Flask is accessible externally
