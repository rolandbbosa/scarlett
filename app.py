from flask import Flask, jsonify
import requests
import random

# Initialize the Flask application
app = Flask(__name__)

# Load the data from the specified URL
def load_data():
    url = "https://raw.githubusercontent.com/rolandbbosa/scarlett/refs/heads/main/brain.json"  # Replace with the actual URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to load data from URL: {e}"}
    except ValueError:
        return {"error": "Failed to decode JSON from the URL"}

# Route to get all the controversial phrases
@app.route('/api/data', methods=['GET'])
def get_data():
    data = load_data()
    return jsonify(data)

# Route to get controversial phrases for a specific category
@app.route('/api/data/<category>', methods=['GET'])
def get_category_data(category):
    data = load_data()
    if category in data:
        return jsonify(data[category])
    else:
        return jsonify({"error": f"Category '{category}' not found"}), 404

# Root route to display a random topic with a random controversial phrase
@app.route('/')
def random_topic_and_phrase():
    data = load_data()
    if "error" in data:
        return jsonify(data)  # Return error if loading data failed
    
    # Select a random category
    category = random.choice(list(data.keys()))
    phrases = data[category].get("controversial_phrases", [])
    
    if phrases:
        # Select a random controversial phrase from the chosen category
        phrase = random.choice(phrases)
        return jsonify({
            "category": category,
            "controversial_phrase": phrase
        })
    else:
        return jsonify({
            "error": f"No controversial phrases found in category '{category}'"
        })

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
