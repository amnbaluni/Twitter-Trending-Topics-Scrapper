# Import necessary modules from Flask and MongoDB libraries
from flask import Flask, render_template
from pymongo import MongoClient
import subprocess
from bson.json_util import dumps
from bson import ObjectId

# Create a Flask web application
app = Flask(__name__)

# Connect to the MongoDB database running on localhost at port 27017
client = MongoClient('mongodb://localhost:27017/')

# Select the 'twitter_trends' database
db = client['twitter_trends']

# Select the 'trends' collection within the 'twitter_trends' database
collection = db['trends']

# Define a route for the root URL ("/")
@app.route('/')
def index():
    """
    This function renders the index.html template.

    Parameters:
    None

    Returns:
    render_template('index.html'): The rendered index.html template.
    """
    return render_template('index.html')

# Define a route for the "/run-script" URL
@app.route('/run-script')
def run_script():
    
    result = subprocess.run(["python", "selenium_script.py"], capture_output=True, text=True)
    
    latest_record = collection.find().sort([('_id', -1)]).limit(1)
    if collection.count_documents({}) == 0:
        return "No records found. Please run the script again."

    latest_record = latest_record[0]
    latest_record['_id'] = str(latest_record['_id'])  # Convert ObjectId to string
    
    return render_template('result.html', record=dumps(latest_record))

# Run the Flask web application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
