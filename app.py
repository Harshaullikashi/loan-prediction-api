from flask import Flask, request, jsonify
import pickle

# Initialize Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return "🏦 Loan Approval API is running!"

# Load ML model
try:
    model = pickle.load(open("loan_model.pkl", "rb"))
    print("✅ Model loaded successfully")
except Exception as e:
    print("🚨 Error loading model:", e)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        prediction = model.predict([[data["Income"], data["Credit_Score"], data["Loan_Amount"]]])
        return jsonify({"Loan_Approval": "✅ Approved" if prediction[0] else "❌ Not Approved"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Registered Routes:", app.url_map)  # Debugging print
    app.run(debug=True)
