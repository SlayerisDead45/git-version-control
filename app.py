from flask import Flask, render_template, request, redirect, jsonify
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environmental configurations securely
load_dotenv()

app = Flask(__name__)

# --- Requirement 1: File-based Local API Route ---
@app.route('/api')
def api_route():
    with open('data.json', 'r') as f:
        my_data = json.load(f)
    return jsonify(my_data)

# --- Requirement 2: Frontend Form Landing Page ---
@app.route('/')
def home():
    return render_template('index.html')

# --- Requirement 2: Form Handler & MongoDB Atlas Integration ---
@app.route('/submit', methods=['POST'])
def handle_form():
    user_text = request.form.get('content')
    
    if not user_text:
        return render_template('index.html', error_msg="Error: The box is empty!")

    try:
        # Secure link fetched directly from your local hidden .env file
        uri = os.getenv("MONGO_URI")
        client = MongoClient(uri)
        db = client.my_database
        
        # Save record to cloud collection
        db.my_collection.insert_one({"info": user_text})
        
        # Redirect pattern triggered upon success
        return redirect('/success')
        
    except Exception as e:
        # Error stays on the same page view without redirecting the user
        return render_template('index.html', error_msg=f"Database Error: {e}")

@app.route('/success')
def success():
    return "Data submitted successfully"

if __name__ == '__main__':
    app.run(debug=True)