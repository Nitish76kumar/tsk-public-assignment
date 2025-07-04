# webhook-repo

Flask server to receive GitHub webhook events, store them in MongoDB, and display them in a minimal UI.

---

## 🚀 Features

- Receives GitHub webhooks for:
  - `push`
  - `pull_request`
  - (supports merge detection via closed PRs)
- Stores events in MongoDB
- Minimal HTML/JS UI that polls every 15 seconds to show the latest events

---

## ⚙️ Tech Stack

- Python 3
- Flask
- PyMongo
- MongoDB Atlas (recommended)
- HTML + JS frontend

---


