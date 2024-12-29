from flask import Flask, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId 
from main import fetch_trending_topics  

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "twitter_data"
MONGO_COLLECTION = "trending_topics"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-script", methods=["GET"])
def run_script():
    try:
        
        fetch_trending_topics()
        return jsonify({"status": "success", "message": "Script executed successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/get-latest-results", methods=["GET"])
def get_latest_results():
    try:
        with MongoClient(MONGO_URI) as client:
            db = client[MONGO_DB]
            collection = db[MONGO_COLLECTION]
            latest_record = collection.find_one(sort=[("_id", -1)])  
            if latest_record:
                
                latest_record["_id"] = str(latest_record["_id"])
                return jsonify(latest_record)
            else:
                return jsonify({"status": "error", "message": "No records found in the database."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
