from flask import Flask, render_template
from pymongo import MongoClient
import subprocess
from bson.json_util import dumps
from bson import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trends']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    
    result = subprocess.run(["python", "selenium_script.py"], capture_output=True, text=True)
    
    latest_record = collection.find().sort([('_id', -1)]).limit(1)
    if collection.count_documents({}) == 0:
        return "No records found. Please run the script again."

    latest_record = latest_record[0]
    latest_record['_id'] = str(latest_record['_id'])  # Convert ObjectId to string
    
    return render_template('result.html', record=dumps(latest_record))

if __name__ == '__main__':
    app.run(debug=True)
