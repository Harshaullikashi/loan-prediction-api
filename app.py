from flask import Flask, request, jsonify
import pickle

# Initialize Flask App
app = Flask(__name__)  

# Load ML Model
model = pickle.load(open("loan_model.pkl", "rb"))  

@app.route('/')
def home():
    return "🏦 Loan Approval API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json  # Extract JSON input

        # Convert input data into a list for prediction
        input_features = [[data["Income"], data["Credit_Score"], data["Loan_Amount"]]]
        
        prediction = model.predict(input_features)  # Use ML model
        
        return jsonify({"Loan_Approval": "✅ Approved" if prediction[0] else "❌ Not Approved"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)  # Enable debugging for easier troubleshooting

