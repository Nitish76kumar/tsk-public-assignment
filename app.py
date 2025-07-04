import os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client.webhooks
events = db.events

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    author = None
    from_branch = None
    to_branch = None
    timestamp = datetime.utcnow().isoformat() + 'Z'

    if event_type == "push":
        author = payload.get('pusher', {}).get('name')
        to_branch = payload.get('ref', '').split('/')[-1]
        event = "PUSH"

    elif event_type == "pull_request":
        pr = payload.get('pull_request', {})
        author = pr.get('user', {}).get('login')
        from_branch = pr.get('head', {}).get('ref')
        to_branch = pr.get('base', {}).get('ref')
        if payload.get('action') == "closed" and pr.get('merged'):
            event = "MERGE"
        else:
            event = "PULL_REQUEST"

    else:
        return jsonify({"status": "ignored", "reason": "unsupported event"}), 400

    doc = {
        "author": author,
        "event": event,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": timestamp
    }

    events.insert_one(doc)
    return jsonify({"status": "success", "data": doc}), 200

@app.route('/events')
def get_events():
    last_events = list(events.find().sort('_id', -1).limit(20))
    for e in last_events:
        e['_id'] = str(e['_id'])
    return jsonify(last_events)

if __name__ == "__main__":
    app.run(debug=True)
